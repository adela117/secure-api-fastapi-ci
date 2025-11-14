# Secure API Starter (FastAPI + DevSecOps)

![CI](https://img.shields.io/github/actions/workflow/status/adela117/pg-secure-api/ci.yml?label=CI)
![License](https://img.shields.io/badge/license-MIT-informational)
![Security](https://img.shields.io/badge/SBOM-CycloneDX-blue)
![DAST](https://img.shields.io/badge/DAST-ZAP%20baseline-purple)

Production-minded FastAPI template:
- ✅ Unit tests (pytest)
- ✅ Code style (Black + Flake8)
- ✅ Dockerized runtime
- ✅ SBOM (CycloneDX via Syft) + dependency audit (pip-audit)
- ✅ ZAP baseline scan on `/health`

## Quick start

```bash
# 1) run locally
pip install -r requirements.txt
uvicorn app.main:app --reload

# 2) or run in Docker
docker build -t secure-api .
docker run -p 8000:8000 secure-api
