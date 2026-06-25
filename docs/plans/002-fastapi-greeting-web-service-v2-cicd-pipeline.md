# CI/CD Pipeline — FastAPI Greeting Web Service v2

Plan ID: `002-fastapi-greeting-web-service-v2`

## Overview

A five-stage pipeline runs on every push and pull request, gates deploys on a
green build, and requires manual approval before promoting to production.

```
lint → test → build → security-scan → deploy
```

## Trigger Rules

| Event              | Branches      | Stages that run                           |
|--------------------|---------------|-------------------------------------------|
| Push               | `main`, `dev` | lint, test, build, security-scan, deploy* |
| Pull request       | any → `main`  | lint, test, build, security-scan          |

*Deploy requires manual approval (GitHub Environment protection rule).

## Stages

### 1 — Lint

Tool: **ruff**

```bash
uv run ruff check .
uv run ruff format --check .
```

Fails fast; no further stages run on lint failure.

### 2 — Test

Tool: **pytest** with **pytest-cov**

```bash
uv run pytest --cov=hello_python --cov-report=xml --cov-report=term-missing
```

- Runs all three lanes: `tests/unit/`, `tests/api/`, `tests/integration/`.
- Coverage XML report uploaded as a build artefact and posted to the PR (via
  `coverage-comment` action or equivalent).
- Build fails if coverage drops below **80%** (`fail_under = 80` in
  `pyproject.toml`).

### 3 — Build

Tool: **Docker buildx**

```bash
docker buildx build \
  --file Dockerfile \
  --tag ghcr.io/${{ github.repository }}:${{ github.sha }} \
  --cache-from type=gha \
  --cache-to   type=gha,mode=max \
  --load \
  .
```

- Multi-stage Dockerfile produces a slim runtime image.
- Layer cache stored in the GitHub Actions cache backend.
- Image is saved as a `.tar` artefact so the security-scan stage can inspect it
  without re-pulling from a registry.

### 4 — Security Scan

Tool: **Trivy** (via `aquasecurity/trivy-action`)

```yaml
- uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
    format: sarif
    output: trivy-results.sarif
    severity: CRITICAL,HIGH
    exit-code: '1'
```

- Fails the build on `CRITICAL` or `HIGH` findings.
- SARIF report uploaded to GitHub Security tab.

### 5 — Deploy

Controlled by a **GitHub Environment** named `production` with a required
reviewer (manual approval gate).

```bash
# Push image to registry after approval
docker push ghcr.io/${{ github.repository }}:${{ github.sha }}

# Optional: rolling restart on target cluster
# kubectl rollout restart deployment/hello-python --namespace production
```

- Only runs after all previous stages pass **and** a designated reviewer
  approves via GitHub's environment-protection UI.
- Runs on `main` branch pushes only; PRs never trigger the deploy stage.

## Artefacts Published

| Artefact            | Retention | Description                              |
|---------------------|-----------|------------------------------------------|
| `coverage.xml`      | 14 days   | pytest-cov XML for PR coverage comments  |
| `trivy-results.sarif` | 30 days | Security scan report (GitHub Security)   |

## Environment Variables / Secrets

| Name                    | Scope      | Description                              |
|-------------------------|------------|------------------------------------------|
| `GITHUB_TOKEN`          | auto       | Push to GHCR, upload SARIF               |

No application secrets are needed: all endpoints are public and read-only.

## Local Equivalence

Developers can reproduce every CI stage locally:

```bash
# Lint
uv run ruff check . && uv run ruff format --check .

# Test + coverage
uv run pytest --cov=hello_python --cov-report=term-missing

# Build
docker build -t hello-python:local .

# Security scan (requires trivy CLI)
trivy image hello-python:local
```
