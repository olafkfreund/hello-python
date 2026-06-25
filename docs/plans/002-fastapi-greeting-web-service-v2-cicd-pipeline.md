# CI/CD Pipeline — FastAPI Greeting Web Service v2

**Plan ID:** 002-fastapi-greeting-web-service-v2-cicd-pipeline  
**Service:** hello-python (FastAPI greeting web service)  
**Platform:** GitHub Actions

---

## Overview

This document specifies the CI/CD pipeline for the FastAPI greeting web service v2. The pipeline
runs on every push and pull request, enforcing code quality, test coverage, image hygiene, and
security before any artifact reaches a deployment environment.

Pipeline shape: **lint → test → build → security-scan → deploy**

---

## Trigger Strategy

| Event | Branches | Pipeline stages |
|---|---|---|
| `push` | `main`, `master` | All stages (deploy skipped unless env is configured) |
| `pull_request` | `main`, `master` | lint, test, build, security-scan (no deploy) |

---

## Stages

### 1. Lint

**Tool:** [Ruff](https://docs.astral.sh/ruff/)  
**Commands:**
```bash
ruff check .
ruff format --check .
```

Checks:
- PEP 8 style (`E`)
- Pyflakes errors (`F`)
- Import ordering (`I`)

Fails fast: any lint error blocks subsequent stages.

---

### 2. Test

**Tool:** pytest + pytest-cov  
**Commands:**
```bash
pytest --cov=hello_python --cov-report=xml --cov-report=term-missing -q
```

Coverage target: **≥ 80%** of `hello_python/`.

Artefacts published:
- `coverage.xml` — uploaded to the workflow run and (optionally) to Codecov.
- JUnit XML report for GitHub test summary.

Lanes exercised:
- `tests/unit/` — pure logic, no I/O
- `tests/api/` — FastAPI TestClient (in-process)
- `tests/integration/` — startup / Dockerfile contract checks

---

### 3. Build

**Tool:** Docker  
**Commands:**
```bash
docker build -t hello-python:ci .
docker tag hello-python:ci hello-python:${GITHUB_SHA::8}
```

The built image is saved as a tarball artefact so the security-scan stage can reuse it without
rebuilding.

---

### 4. Security Scan

**Tools:**
- **pip-audit** — scans Python dependencies against OSV / PyPI advisory databases.
- **Trivy** — scans the Docker image for OS and language CVEs.

**Commands:**
```bash
pip-audit --requirement requirements.txt --strict
trivy image --exit-code 1 --severity HIGH,CRITICAL hello-python:ci
```

`pip-audit` runs against a pinned `requirements.txt` exported from the lockfile. Trivy uses the
image tarball produced in the Build stage.

Failures block the deploy stage.

---

### 5. Deploy

**Environments:**
| Environment | Trigger | Approval |
|---|---|---|
| `staging` | Push to `main` after green build | Automatic |
| `production` | Push to `main` after green staging | Manual approval required |

Deploy is **not** triggered on pull requests.

GitHub environment protection rules enforce the manual approval gate on `production`. Reviewers
listed in the environment settings must approve before the job runs.

**Deployment action:** push the tagged image to the container registry and roll out via
`kubectl set image` (or equivalent GitOps path).

---

## Secrets & Environment Variables

| Secret / Var | Used in | Purpose |
|---|---|---|
| `REGISTRY_URL` | build, deploy | Container registry host |
| `REGISTRY_USER` | build, deploy | Registry auth username |
| `REGISTRY_PASSWORD` | build, deploy | Registry auth token |
| `KUBECONFIG` | deploy | Cluster credentials |

All secrets are stored in GitHub repository or environment secrets — never in the repository.

---

## Acceptance Criteria

- [ ] Lint, test, build, and security-scan stages run on every push and PR.
- [ ] The test stage runs the full suite and publishes a coverage report.
- [ ] Deploy stages are gated on a green build and require manual approval (production).
