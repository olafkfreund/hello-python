"""
FastAPI greeting web service.

Access control note: all endpoints are public and read-only, hold no secrets,
and perform no writes — access control is explicitly out of scope for this
service. The ``/healthz`` readiness probe is intentionally left unauthenticated
so orchestrators can call it, so its response body is restricted to dependency
names and a ready/not-ready status and never leaks connection details.
"""

import os
import socket
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path, Response

app = FastAPI(title="hello-python", version="0.1.0")

# Comma-separated list of dependencies to probe for readiness, each written as
# ``name=host:port`` (e.g. ``db=db.internal:5432,cache=cache.internal:6379``).
# Read at request time so deployments (and tests) can reconfigure it without a
# process restart. When unset, no dependencies are configured and readiness is
# reported as soon as the process itself is up.
HEALTHZ_DEPENDENCIES_ENV = "HEALTHZ_DEPENDENCIES"

# Per-dependency round-trip timeout, in seconds. Kept short so the readiness
# probe stays responsive even when a dependency is hanging rather than refusing.
HEALTHZ_TIMEOUT_SECONDS = 2.0


def _configured_dependencies() -> list[tuple[str, str, int]]:
    """Parse the configured dependencies into ``(name, host, port)`` tuples.

    Malformed entries are skipped rather than raised, so a configuration typo
    can never crash the probe (and never surface as an error body).
    """
    raw = os.environ.get(HEALTHZ_DEPENDENCIES_ENV, "").strip()
    dependencies: list[tuple[str, str, int]] = []
    if not raw:
        return dependencies
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        name, sep, target = entry.partition("=")
        if not sep:
            continue
        host, sep, port = target.rpartition(":")
        if not sep:
            continue
        try:
            port_number = int(port)
        except ValueError:
            continue
        name = name.strip()
        host = host.strip()
        if not name or not host:
            continue
        dependencies.append((name, host, port_number))
    return dependencies


def _check_dependency(host: str, port: int) -> None:
    """Perform a real round-trip TCP reachability check against a dependency.

    Opens (and immediately closes) a TCP connection to ``host:port``. Raises
    ``OSError`` if the dependency cannot be reached within the timeout — this is
    a genuine round-trip, not a configuration-only check, so a configured but
    unreachable dependency always fails.
    """
    with socket.create_connection((host, port), timeout=HEALTHZ_TIMEOUT_SECONDS):
        pass


def _probe_dependency(host: str, port: int) -> bool:
    """Probe a dependency and return whether it is reachable, sanitizing errors.

    This is the sanitization boundary for the readiness probe: it wraps the
    round-trip check so that *any* error it raises — DNS failures, refused or
    timed-out connections, TLS/driver errors — is caught here and collapsed to a
    single ``False``. No exception object, message, ``host``, ``port``, or driver
    error text ever escapes this function, so callers can only observe a boolean
    and never leak connection details, credentials, or versions into the
    (unauthenticated) response body.
    """
    try:
        _check_dependency(host, port)
    except Exception:  # noqa: BLE001 - sanitize any driver/OS error text
        return False
    return True


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe. Returns HTTP 200 once the process is running.

    Public endpoint — no authentication required, no secrets exposed, read-only.
    """
    return {"status": "ok"}


@app.get("/healthz")
def healthz(response: Response) -> dict[str, object]:
    """Readiness probe. Returns HTTP 200 only when every configured dependency
    passes a real round-trip reachability check; otherwise HTTP 503 naming the
    unreachable dependency (dependencies).

    Any error raised while probing a dependency is caught and reduced to the
    dependency's name so the (unauthenticated) response body never leaks
    hostnames, ports, connection strings, credentials, versions, or driver
    error text.

    Public endpoint — no authentication required, no secrets exposed, read-only.
    """
    unavailable: list[str] = []
    for name, host, port in _configured_dependencies():
        if not _probe_dependency(host, port):
            unavailable.append(name)

    if unavailable:
        response.status_code = 503
        return {
            "status": "not ready",
            "dependencies": {name: "unavailable" for name in unavailable},
        }

    return {"status": "ready"}


@app.get("/greet/{name}")
def greet(
    name: Annotated[
        str,
        Path(max_length=64, description="Name to greet (max 64 characters)"),
    ],
) -> dict[str, str]:
    """Greet endpoint. Returns HTTP 200 with a personalised greeting message.

    The name parameter is length-bounded to 64 characters to prevent abuse.
    Names exceeding this limit return HTTP 422.

    Public endpoint — no authentication required, no secrets exposed, read-only.
    """
    return {"message": f"Hello, {name}!"}


def main() -> None:
    uvicorn.run("hello_python.web:app", host="0.0.0.0", port=8080, reload=False)


if __name__ == "__main__":
    main()
