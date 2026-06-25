# FastAPI greeting web service v2

> Generated from a signed trusted plan (approved by pfactory). The authoritative build artifact is implementation_plan.json.

**Workflow type:** feature

## Acceptance Criteria

- `GET /healthz` returns HTTP 200 with body `{"status": "ok"}`.
- `GET /greet/ada` returns HTTP 200 with body `{"message": "Hello, ada!"}`.
- `GET /greet/{name}` greets any valid provided name correctly (e.g. `/greet/Bob` → `{"message": "Hello, Bob!"}`).
- The `{name}` path parameter is validated: names longer than 64 characters return HTTP 422 (input is length-bounded to prevent abuse).
- Access control is explicitly out of scope: all endpoints are public and read-only, hold no secrets, and perform no writes — documented in the code.
- The app object is importable as `hello_python.web:app` and starts under uvicorn on port 8080.
- A `Dockerfile` exists that builds the service and runs it on port 8080.

## Implementation Plan

### Implementation

- `C1` `GET /healthz` returns HTTP 200 with body `{"status": "ok"}`.
- `C2` `GET /greet/ada` returns HTTP 200 with body `{"message": "Hello, ada!"}`.
- `C3` `GET /greet/{name}` greets any valid provided name correctly (e.g. `/greet/Bob`…

`GET /greet/{name}` greets any valid provided name correctly (e.g. `/greet/Bob` → `{"message": "Hello, Bob!"}`).
- `C4` The `{name}` path parameter is validated: names longer than 64 characters retur…

The `{name}` path parameter is validated: names longer than 64 characters return HTTP 422 (input is length-bounded to prevent abuse).
- `C5` Access control is explicitly out of scope: all endpoints are public and read-on…

Access control is explicitly out of scope: all endpoints are public and read-only, hold no secrets, and perform no writes — documented in the code.
- `C6` The app object is importable as `hello_python.web:app` and starts under uvicorn…

The app object is importable as `hello_python.web:app` and starts under uvicorn on port 8080.
- `C7` A `Dockerfile` exists that builds the service and runs it on port 8080.

### Testing

- `TEST` Set up testing for FastAPI greeting web service v2

Implement the testing strategy specified in `docs/plans/002-fastapi-greeting-web-service-v2-testing-strategy.md`.

Lanes: unit / integration / e2e. Each acceptance criterion is mapped to a test approach in the spec. Hand test generation over to TFactory.
- `CICD` Set up CI/CD for FastAPI greeting web service v2

Implement the CI/CD pipeline specified in `docs/plans/002-fastapi-greeting-web-service-v2-cicd-pipeline.md`.

Stages: lint → test → build → security scan → deploy.
