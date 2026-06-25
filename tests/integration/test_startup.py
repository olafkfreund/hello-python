"""Integration tests: service importability and infrastructure artefacts.

Maps:
  AC#6  – app starts under uvicorn on port 8080 (startup config verified)
  AC#7  – Dockerfile exists and exposes port 8080
"""

import importlib
import inspect
import pathlib


# ---------------------------------------------------------------------------
# AC#6 – uvicorn startup configuration
# ---------------------------------------------------------------------------


def test_main_function_exists() -> None:
    """hello_python.web must expose a 'main' entry-point function (AC#6)."""
    module = importlib.import_module("hello_python.web")
    assert callable(getattr(module, "main", None)), "hello_python.web must expose a callable 'main'"


def test_main_uses_port_8080() -> None:
    """The main() function must bind to port 8080 (AC#6)."""
    module = importlib.import_module("hello_python.web")
    source = inspect.getsource(module.main)
    assert "8080" in source, "main() must configure uvicorn to listen on port 8080"


def test_main_uses_correct_app_path() -> None:
    """The main() function must reference 'hello_python.web:app' (AC#6)."""
    module = importlib.import_module("hello_python.web")
    source = inspect.getsource(module.main)
    assert "hello_python.web:app" in source, (
        "main() must pass 'hello_python.web:app' to uvicorn.run()"
    )


# ---------------------------------------------------------------------------
# AC#7 – Dockerfile
# ---------------------------------------------------------------------------


def _repo_root() -> pathlib.Path:
    """Locate the repository root (the directory that contains 'hello_python/')."""
    here = pathlib.Path(__file__).resolve()
    # Walk up until we find the hello_python package directory.
    for parent in [here, *here.parents]:
        if (parent / "hello_python").is_dir():
            return parent
    raise FileNotFoundError("Could not locate repository root")


def test_dockerfile_exists() -> None:
    """A Dockerfile must exist in the repository root (AC#7)."""
    dockerfile = _repo_root() / "Dockerfile"
    assert dockerfile.exists(), f"Dockerfile not found at {dockerfile}"


def test_dockerfile_exposes_port_8080() -> None:
    """The Dockerfile must EXPOSE port 8080 (AC#7)."""
    dockerfile = _repo_root() / "Dockerfile"
    content = dockerfile.read_text()
    assert "8080" in content, "Dockerfile must reference port 8080"


def test_dockerfile_expose_directive() -> None:
    """The Dockerfile must contain an EXPOSE instruction (AC#7)."""
    dockerfile = _repo_root() / "Dockerfile"
    content = dockerfile.read_text()
    assert any(
        line.strip().startswith("EXPOSE") for line in content.splitlines()
    ), "Dockerfile must contain an EXPOSE directive"
