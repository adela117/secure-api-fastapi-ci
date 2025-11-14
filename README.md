# Secure API (FastAPI · Docker · CI/CD · DevSecOps)

![CI](https://github.com/adela117/pg-secure-api/actions/workflows/ci.yml/badge.svg)

A tiny but production-style API to demonstrate a secure software delivery pipeline:
- FastAPI app with health and echo endpoints
- Containerized build (Docker) with live health probe
- CI gates: Unit tests · CodeQL (SAST) · ZAP baseline (DAST) · SBOM (CycloneDX) · Python SCA (pip-audit)
- Protected `main` branch with required checks

## Quickstart
Local:
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
# open http://localhost:8000/health
