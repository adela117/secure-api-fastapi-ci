## Dev setup
python -m pip install -r requirements.txt -r requirements-dev.txt
black . && flake8 . && pytest -q
