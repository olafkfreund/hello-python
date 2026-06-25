"""API tests for hello_python — uses FastAPI's synchronous TestClient.

Each test maps to a plan acceptance criterion:

AC#1  GET /healthz → 200 {"status": "ok"}
AC#2  GET /greet/ada → 200 {"message": "Hello, ada!"}
AC#3  GET /greet/{name} → 200 {"message": "Hello, <name>!"}
AC#4  GET /greet/<name > 64 chars> → 422
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthz:
    """AC#1 — GET /healthz returns HTTP 200 with body {"status": "ok"}."""

    def test_status_code_is_200(self, client: TestClient) -> None:
        response = client.get("/healthz")
        assert response.status_code == 200

    def test_response_body(self, client: TestClient) -> None:
        response = client.get("/healthz")
        assert response.json() == {"status": "ok"}

    def test_content_type_is_json(self, client: TestClient) -> None:
        response = client.get("/healthz")
        assert "application/json" in response.headers["content-type"]


class TestGreetAda:
    """AC#2 — GET /greet/ada returns HTTP 200 with body {"message": "Hello, ada!"}."""

    def test_status_code_is_200(self, client: TestClient) -> None:
        response = client.get("/greet/ada")
        assert response.status_code == 200

    def test_response_body(self, client: TestClient) -> None:
        response = client.get("/greet/ada")
        assert response.json() == {"message": "Hello, ada!"}


class TestGreetName:
    """AC#3 — GET /greet/{name} greets any valid name correctly."""

    @pytest.mark.parametrize(
        "name,expected_message",
        [
            ("Bob", "Hello, Bob!"),
            ("Alice", "Hello, Alice!"),
            ("ada", "Hello, ada!"),
            ("World", "Hello, World!"),
            ("a", "Hello, a!"),
            ("x" * 64, f"Hello, {'x' * 64}!"),  # boundary: exactly 64 chars
        ],
    )
    def test_greet_valid_name(
        self, client: TestClient, name: str, expected_message: str
    ) -> None:
        response = client.get(f"/greet/{name}")
        assert response.status_code == 200
        assert response.json() == {"message": expected_message}

    def test_message_key_present(self, client: TestClient) -> None:
        response = client.get("/greet/TestUser")
        body = response.json()
        assert "message" in body

    def test_greeting_format(self, client: TestClient) -> None:
        """Greeting must follow the pattern 'Hello, <name>!'."""
        name = "TestUser"
        response = client.get(f"/greet/{name}")
        assert response.json()["message"] == f"Hello, {name}!"


class TestGreetValidation:
    """AC#4 — names longer than 64 chars return HTTP 422."""

    def test_name_65_chars_returns_422(self, client: TestClient) -> None:
        long_name = "a" * 65
        response = client.get(f"/greet/{long_name}")
        assert response.status_code == 422

    def test_name_100_chars_returns_422(self, client: TestClient) -> None:
        long_name = "b" * 100
        response = client.get(f"/greet/{long_name}")
        assert response.status_code == 422

    def test_name_64_chars_is_valid(self, client: TestClient) -> None:
        """Boundary value — exactly 64 characters must be accepted (AC#4 boundary)."""
        name_64 = "c" * 64
        response = client.get(f"/greet/{name_64}")
        assert response.status_code == 200

    def test_422_response_has_detail(self, client: TestClient) -> None:
        """FastAPI validation errors must include a 'detail' field."""
        long_name = "z" * 65
        response = client.get(f"/greet/{long_name}")
        body = response.json()
        assert "detail" in body
