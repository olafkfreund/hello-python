# Testing Strategy — FastAPI Greeting Web Service v2

Plan ID: `002-fastapi-greeting-web-service-v2`

## Overview

Three test lanes cover every acceptance criterion (AC#1–AC#7):

| Lane        | Directory              | Framework     | Coverage target |
|-------------|------------------------|---------------|-----------------|
| unit        | `tests/unit/`          | pytest        | ≥80%            |
| api         | `tests/api/`           | pytest + HTTPX| ≥80%            |
| integration | `tests/integration/`   | pytest + HTTPX| ≥80%            |

## Acceptance Criteria → Test Mapping

| AC   | Description                                           | Lane(s)           | Test file / class           |
|------|-------------------------------------------------------|-------------------|-----------------------------|
| AC#1 | `GET /healthz` → 200 `{"status":"ok"}`               | api, integration  | `TestHealthz`, `TestFullStack` |
| AC#2 | `GET /greet/ada` → 200 `{"message":"Hello, ada!"}`   | api, integration  | `TestGreetAda`, `TestFullStack` |
| AC#3 | `GET /greet/{name}` greets any valid name             | api, integration  | `TestGreetName`, `TestFullStack` |
| AC#4 | Names > 64 chars → 422                                | api, integration  | `TestGreetValidation`, `TestFullStack` |
| AC#5 | Access control documented in code                     | unit              | `TestAccessControlDocumentation` |
| AC#6 | App importable as `hello_python.web:app`              | unit              | `TestAppImport` |
| AC#7 | Dockerfile exists, exposes port 8080                  | unit              | `TestDockerfile` |

## Running the Tests

```bash
# Full suite
uv run pytest

# By lane
uv run pytest -q tests/unit
uv run pytest -q tests/api
uv run pytest -q tests/integration

# With coverage report
uv run pytest --cov=hello_python --cov-report=term-missing
```

## Coverage Targets

- Overall source coverage: **≥80%** (enforced via `[tool.coverage.report] fail_under = 80`)
- Coverage measurement targets `src/hello_python/`

## Fixtures

All lanes share a session-scoped `TestClient` fixture defined in `tests/conftest.py`.
This avoids repeated ASGI startup overhead and ensures test isolation at the request level.

## Notes

- No real network sockets are opened; `TestClient` uses the ASGI transport layer directly.
- E2E lane (Dockerfile / container tests) is out of scope for automated CI; the `TestDockerfile`
  unit tests verify the Dockerfile's static content instead.
- The `StarletteDeprecationWarning` about `httpx` vs `httpx2` is emitted by the installed
  `fastapi` package and is suppressed by adding it to `filterwarnings` if required.
