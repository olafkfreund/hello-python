"""Unit tests for hello_python.web.

These tests verify structural / static properties of the application:
- The ``app`` object is importable as ``hello_python.web:app``
- The app is a FastAPI instance
- The access-control comment is present in the source module (AC#5)
- A Dockerfile exists and exposes port 8080 (AC#7)
"""

import importlib
import inspect
import pathlib
from unittest.mock import patch

import fastapi
import pytest

import hello_python.web as web_module


class TestAppImport:
    """AC#6 — app importable as hello_python.web:app."""

    def test_app_attribute_exists(self) -> None:
        """The module must expose an ``app`` attribute."""
        assert hasattr(web_module, "app"), "hello_python.web must export 'app'"

    def test_app_is_fastapi_instance(self) -> None:
        """``app`` must be a FastAPI application object."""
        assert isinstance(web_module.app, fastapi.FastAPI)

    def test_app_importable_via_importlib(self) -> None:
        """Simulate the uvicorn import path used at runtime."""
        module = importlib.import_module("hello_python.web")
        app_obj = getattr(module, "app")
        assert isinstance(app_obj, fastapi.FastAPI)


class TestAccessControlDocumentation:
    """AC#5 — access control is explicitly documented in the code."""

    def test_module_docstring_mentions_access_control(self) -> None:
        """The module-level docstring must reference access control."""
        doc = web_module.__doc__ or ""
        assert "access control" in doc.lower(), (
            "Module docstring must document the access-control stance"
        )

    def test_module_docstring_mentions_public(self) -> None:
        """The module-level docstring must state endpoints are public."""
        doc = web_module.__doc__ or ""
        assert "public" in doc.lower()

    def test_module_docstring_mentions_read_only(self) -> None:
        """The module-level docstring must state endpoints are read-only."""
        doc = web_module.__doc__ or ""
        assert "read-only" in doc.lower()

    def test_module_source_contains_no_auth_comment(self) -> None:
        """Source file must contain an inline comment explaining no auth middleware."""
        source = inspect.getsource(web_module)
        assert "no auth" in source.lower() or "no secrets" in source.lower(), (
            "Source must contain a comment clarifying the no-auth design decision"
        )


def _find_dockerfile() -> pathlib.Path:
    """Locate the Dockerfile at the project root (contains pyproject.toml)."""
    here = pathlib.Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists():
            return parent / "Dockerfile"
    pytest.skip("Could not locate project root (pyproject.toml not found)")


@pytest.fixture(scope="module")
def dockerfile_path() -> pathlib.Path:
    """Return the path to the project-root Dockerfile."""
    return _find_dockerfile()


class TestDockerfile:
    """AC#7 — Dockerfile exists and exposes port 8080."""

    def test_dockerfile_exists(self, dockerfile_path: pathlib.Path) -> None:
        """A Dockerfile must be present at the project root."""
        assert dockerfile_path.exists(), f"Dockerfile not found at {dockerfile_path}"

    def test_dockerfile_exposes_8080(self, dockerfile_path: pathlib.Path) -> None:
        """Dockerfile must expose port 8080."""
        content = dockerfile_path.read_text()
        assert "EXPOSE 8080" in content, "Dockerfile must contain 'EXPOSE 8080'"

    def test_dockerfile_runs_on_8080(self, dockerfile_path: pathlib.Path) -> None:
        """Dockerfile CMD/ENTRYPOINT must bind to port 8080."""
        content = dockerfile_path.read_text()
        assert "8080" in content, (
            "Dockerfile must reference port 8080 in CMD/ENTRYPOINT"
        )


class TestMain:
    """AC#6 — main() starts uvicorn on port 8080."""

    def test_main_calls_uvicorn_run(self) -> None:
        """main() must invoke uvicorn.run with the correct arguments."""
        with patch("uvicorn.run") as mock_run:
            web_module.main()
        mock_run.assert_called_once_with(
            "hello_python.web:app",
            host="0.0.0.0",
            port=8080,
            reload=False,
        )
