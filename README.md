# Secure API Starter (FastAPI + CI/DC + Security)

![CI](https://img.shields.io/github/actions/workflow/status/adela117/pg-secure-api/ci.yml?label=CI)
![License](https://img.shields.io/badge/license-MIT-informational)
![Security](https://img.shields.io/badge/SBOM-CycloneDX-blue)
![DAST](https://img.shields.io/badge/DAST-ZAP%20baseline-purple)

Production-minded FastAPI template:
- ✅ Tests run on every push/PR (pytest)
- ✅ Code style is enforced (Black + Flake8)
- ✅ App builds and runs in Docker
- ✅ SBOM is generated (CycloneDX) and dependencies are audited (pip-audit)
- ✅ A lightweight ZAP scan hits the health endpoint to catch obvious issues

## Quick start

```bash
# 1) run locally
pip install -r requirements.txt
uvicorn app.main:app --reload

# 2) or run in Docker
docker build -t secure-api .
docker run -p 8000:8000 secure-api
