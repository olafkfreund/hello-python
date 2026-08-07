"""API-level tests covering every acceptance criterion via the TestClient.

Maps:
  AC#1  – GET /healthz → 200 {"status": "ok"}
  AC#2  – GET /greet/ada → 200 {"message": "Hello, ada!"}
  AC#3  – GET /greet/{name} greets any valid name
  AC#4  – names > 64 chars → 422
  AC#5  – access-control comment is present in the module docstring
  AC#6  – app is importable as hello_python.web:app
"""

import importlib

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# AC#1 – health checks: /health liveness + /healthz readiness
# ---------------------------------------------------------------------------


def test_health_returns_200(client: TestClient) -> None:
    """GET /health (liveness) must return HTTP 200 (AC#1)."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_status_ok(client: TestClient) -> None:
    """GET /health body must be {"status": "ok"} (AC#1)."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_unaffected_by_healthz_dependency_failure(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """GET /health (liveness) must stay 200 {"status": "ok"} regardless of the
    /healthz readiness logic.

    Even when a dependency is configured at an unreachable address — the exact
    condition that makes /healthz return 503 — the liveness endpoint must be
    completely unaffected and keep returning 200 {"status": "ok"}. This proves
    the new readiness logic did not alter the existing /health contract.
    """
    monkeypatch.setenv("HEALTHZ_DEPENDENCIES", "db=127.0.0.1:1")

    # Sanity check: /healthz genuinely fails under this configuration.
    assert client.get("/healthz").status_code == 503

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_healthz_returns_200(client: TestClient) -> None:
    """GET /healthz (readiness) must return HTTP 200 when all deps reachable."""
    response = client.get("/healthz")
    assert response.status_code == 200


def test_healthz_returns_status_ready(client: TestClient) -> None:
    """GET /healthz body must be {"status": "ready"} when all deps reachable."""
    response = client.get("/healthz")
    assert response.json() == {"status": "ready"}


def test_healthz_returns_503_when_dependency_unreachable(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """GET /healthz must return HTTP 503 when a configured dependency is
    unreachable.

    This is the key test proving the readiness check can actually fail rather
    than passing vacuously: pointing a dependency at an address nothing is
    listening on (127.0.0.1:1) forces the round-trip check to fail, and the
    endpoint must report 503 and name the failing dependency ("db").
    """
    monkeypatch.setenv("HEALTHZ_DEPENDENCIES", "db=127.0.0.1:1")

    response = client.get("/healthz")

    assert response.status_code == 503
    assert "db" in response.json()["dependencies"]


def test_healthz_503_body_names_dependency_without_leaking_details(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The 503 body must name the failing dependency but leak no connection
    details.

    Point a dependency at an unreachable target whose host, port and
    credentials are distinctive strings, then assert the response body contains
    the dependency name ("db") but none of the forbidden fields: hostnames,
    ports, connection strings, credentials, versions, or driver error text.
    """
    host = "secret-db-host.internal.example"
    port = "54329"
    user = "admin"
    password = "s3cr3t-p4ssw0rd"
    monkeypatch.setenv(
        "HEALTHZ_DEPENDENCIES",
        f"db=postgresql://{user}:{password}@{host}:{port}",
    )

    response = client.get("/healthz")

    assert response.status_code == 503
    # The failing dependency is named so callers know which one is not ready.
    assert "db" in response.json()["dependencies"]

    # No connection details, credentials, versions, or driver error text may
    # appear anywhere in the (unauthenticated) response body.
    body = response.text
    forbidden = [
        host,
        "secret-db-host",
        "internal",
        "example",
        port,
        user,
        password,
        "postgresql",
        "Connection refused",
        "ConnectionRefusedError",
        "OSError",
        "socket",
        "timed out",
        "getaddrinfo",
        "Errno",
        "Traceback",
    ]
    for token in forbidden:
        assert token not in body, f"forbidden token leaked in body: {token!r}"


# ---------------------------------------------------------------------------
# AC#2 – greet the canonical name "ada"
# ---------------------------------------------------------------------------


def test_greet_ada_returns_200(client: TestClient) -> None:
    """GET /greet/ada must return HTTP 200 (AC#2)."""
    response = client.get("/greet/ada")
    assert response.status_code == 200


def test_greet_ada_body(client: TestClient) -> None:
    """GET /greet/ada body must be {"message": "Hello, ada!"} (AC#2)."""
    response = client.get("/greet/ada")
    assert response.json() == {"message": "Hello, ada!"}


# ---------------------------------------------------------------------------
# AC#3 – greet any valid name
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "name,expected_message",
    [
        ("Bob", "Hello, Bob!"),
        ("Alice", "Hello, Alice!"),
        ("world", "Hello, world!"),
        ("X" * 64, f"Hello, {'X' * 64}!"),  # boundary: exactly 64 chars
    ],
)
def test_greet_arbitrary_name(
    client: TestClient, name: str, expected_message: str
) -> None:
    """GET /greet/{name} greets any valid name correctly (AC#3)."""
    response = client.get(f"/greet/{name}")
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}


# ---------------------------------------------------------------------------
# AC#4 – name length validation
# ---------------------------------------------------------------------------


def test_greet_name_too_long_returns_422(client: TestClient) -> None:
    """GET /greet/{name} with a 65-char name must return HTTP 422 (AC#4)."""
    long_name = "A" * 65
    response = client.get(f"/greet/{long_name}")
    assert response.status_code == 422


def test_greet_name_max_length_valid(client: TestClient) -> None:
    """GET /greet/{name} with a 64-char name must succeed (AC#4 boundary)."""
    name = "B" * 64
    response = client.get(f"/greet/{name}")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# AC#5 – access-control documentation
# ---------------------------------------------------------------------------


def test_access_control_documented_in_module() -> None:
    """The web module docstring must document that all endpoints are public (AC#5)."""
    import hello_python.web as web_module  # noqa: PLC0415

    doc = web_module.__doc__ or ""
    assert "public" in doc.lower(), (
        "Module docstring must mention that endpoints are public"
    )
    assert "read-only" in doc.lower(), (
        "Module docstring must mention that endpoints are read-only"
    )
    assert "access control" in doc.lower(), (
        "Module docstring must address access control"
    )


# ---------------------------------------------------------------------------
# AC#6 – app importable as hello_python.web:app
# ---------------------------------------------------------------------------


def test_app_importable() -> None:
    """hello_python.web must export an 'app' object (AC#6)."""
    module = importlib.import_module("hello_python.web")
    assert hasattr(module, "app"), "hello_python.web must expose 'app'"


def test_app_is_fastapi_instance() -> None:
    """hello_python.web:app must be a FastAPI application (AC#6)."""
    from fastapi import FastAPI  # noqa: PLC0415

    from hello_python.web import app  # noqa: PLC0415

    assert isinstance(app, FastAPI)
