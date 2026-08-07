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


def test_healthz_returns_200(client: TestClient) -> None:
    """GET /healthz (readiness) must return HTTP 200 when all deps reachable."""
    response = client.get("/healthz")
    assert response.status_code == 200


def test_healthz_returns_status_ready(client: TestClient) -> None:
    """GET /healthz body must be {"status": "ready"} when all deps reachable."""
    response = client.get("/healthz")
    assert response.json() == {"status": "ready"}


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
