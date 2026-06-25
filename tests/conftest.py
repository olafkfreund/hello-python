"""Shared pytest fixtures for the hello_python test suite."""

import pytest
from fastapi.testclient import TestClient

from hello_python.web import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Return a TestClient bound to the FastAPI app for the whole session."""
    return TestClient(app)
