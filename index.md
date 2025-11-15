---
title: Secure API FastAPI CI
layout: default
---

# Secure API FastAPI CI

Production-minded FastAPI template validated entirely in GitHub Actions:
tests, lint, container boot & health-check, ZAP baseline DAST, CycloneDX SBOM,
pip-audit, Trivy image scan, Bandit static analysis, Prometheus metrics, and
runtime hardening (API key, rate limit, security headers).

<!-- Contact buttons -->
<p>
  <a href="https://www.linkedin.com/in/albert-de-la-cruz-282-fiu/" target="_blank" rel="noopener noreferrer">
    <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin&logoColor=white">
  </a>
  &nbsp;
  <a href="mailto:delacruz.albert@proton.me">
    <img alt="Email" src="https://img.shields.io/badge/Email-Contact-informational?logo=gmail&logoColor=white">
  </a>
</p>

**Repo:** https://github.com/adela117/secure-api-fastapi-ci

## What’s inside
- ✅ Pytest on every push/PR
- ✅ Black + Flake8 style gates
- ✅ Docker build + health-check in CI
- ✅ ZAP baseline DAST
- ✅ CycloneDX SBOM via Syft + `pip-audit --strict`
- ✅ Trivy image scan (HIGH/CRITICAL fail)
- ✅ Bandit static analysis
- ✅ Prometheus `/metrics` + basic API key auth + rate limit

## Screenshots
![CI green](docs/ci-green.png)

## Quick links
- API docs when running or deployed: `/docs`
- Health: `/health`
- Metrics: `/metrics`

## Contact
- LinkedIn: https://www.linkedin.com/in/albert-de-la-cruz-282-fiu
- Email: delacruz.albert@proton.me
