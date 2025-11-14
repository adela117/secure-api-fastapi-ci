name: ci
on:
  pull_request:
  push:
    branches: ["**"]

# we need write perms so the lint job can auto-commit Black formatting
permissions:
  contents: write
  issues: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements*.txt') }}
          restore-keys: ${{ runner.os }}-pip-
      - run: python -m pip install -r requirements.txt -r requirements-dev.txt
      - run: python -m pytest -q

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements*.txt') }}
          restore-keys: ${{ runner.os }}-pip-
      - name: Install linters
        run: python -m pip install black flake8

      # 1) Format the repo
      - name: Run Black (format)
        run: black .

      # 2) Auto-commit any changes (Black rewrites)
      - name: Commit formatting (if any)
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "style: format with Black"
          commit_user_name: "ci-bot"
          commit_user_email: "ci@example.com"
          commit_author: "ci-bot <ci@example.com>"

      # 3) Verify + lint so the job is still a gate
      - name: Run Black (check)
        run: black --check .
      - name: Run Flake8
        run: flake8 .

  build_and_zap:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v5
        with:
          context: .
          tags: local/secure-api:ci
          load: true
          cache-from: type=gha
          cache-to: type=gha,mode=max
      - name: Run container
        run: |
          docker run -d -p 8000:8000 \
            -e APP_VERSION=${{ github.ref_name }} \
            -e GIT_COMMIT_SHA=${{ github.sha }} \
            --name api local/secure-api:ci
      - name: Wait for health
        run: |
          for i in {1..25}; do
            curl -fsS http://localhost:8000/health && exit 0
            sleep 1
          done
          echo "App never became healthy"; docker logs api || true
          exit 1
      - name: ZAP Baseline DAST
        uses: zaproxy/action-baseline@v0.15.0
        with:
          target: 'http://localhost:8000/health'
          cmd_options: '-I'
      - name: Stop container
        if: always()
        run: docker rm -f api

  sbom_and_deps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate SBOM (CycloneDX via Syft)
        uses: anchore/sbom-action@v0
        with:
          path: .
          format: cyclonedx-json
          output-file: sbom.json
      - uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements*.txt') }}
          restore-keys: ${{ runner.os }}-pip-
      - name: pip-audit (strict)
        run: |
          python -m pip install --upgrade pip
          python -m pip install pip-audit
          pip-audit -r requirements.txt --strict
