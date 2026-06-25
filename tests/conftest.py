"""Shared pytest fixtures for the hello-python test suite."""

import pytest
from fastapi.testclient import TestClient

from hello_python.web import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Return a synchronous HTTPX test client bound to the FastAPI app."""
    with TestClient(app) as c:
        yield c
