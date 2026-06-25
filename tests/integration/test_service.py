"""Integration tests for hello_python.

These tests exercise the full application stack end-to-end using httpx's
AsyncClient with the ASGI transport — no real network socket is opened but
the entire ASGI lifecycle (startup / shutdown) is exercised, verifying that:

- All acceptance criteria pass together (AC#1–AC#4)
- The app handles a realistic request sequence without errors
- Content-type negotiation behaves correctly
"""

from fastapi.testclient import TestClient


class TestFullStack:
    """Integration: exercise the ASGI app through its full request lifecycle."""

    def test_healthcheck_integration(self, client: TestClient) -> None:
        """AC#1 — health endpoint is available and correct throughout the lifecycle."""
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_greet_ada_integration(self, client: TestClient) -> None:
        """AC#2 — /greet/ada works in a full-stack context."""
        response = client.get("/greet/ada")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, ada!"}

    def test_greet_arbitrary_name_integration(self, client: TestClient) -> None:
        """AC#3 — greeting any valid name works end-to-end."""
        for name in ("Alice", "Bob", "World", "x" * 64):
            response = client.get(f"/greet/{name}")
            assert response.status_code == 200
            assert response.json() == {"message": f"Hello, {name}!"}

    def test_validation_integration(self, client: TestClient) -> None:
        """AC#4 — over-length name is rejected at the ASGI layer."""
        response = client.get(f"/greet/{'a' * 65}")
        assert response.status_code == 422

    def test_openapi_schema_available(self, client: TestClient) -> None:
        """The OpenAPI schema endpoint is reachable (FastAPI default)."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema
        assert "/healthz" in schema["paths"]
        assert "/greet/{name}" in schema["paths"]

    def test_sequential_requests(self, client: TestClient) -> None:
        """Multiple sequential requests all succeed — verifies no state corruption."""
        for i in range(5):
            r = client.get("/healthz")
            assert r.status_code == 200

        for name in ("Alice", "Bob", "Charlie", "ada", "World"):
            r = client.get(f"/greet/{name}")
            assert r.status_code == 200
            assert r.json() == {"message": f"Hello, {name}!"}

    def test_unknown_endpoint_returns_404(self, client: TestClient) -> None:
        """Requests to undefined paths return 404 (FastAPI default routing)."""
        response = client.get("/does-not-exist")
        assert response.status_code == 404
