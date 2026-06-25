"""
FastAPI greeting web service.

Access control note: all endpoints are public and read-only, hold no secrets,
and perform no writes — access control is explicitly out of scope for this service.
"""

from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path

app = FastAPI(title="hello-python", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Health check endpoint. Returns HTTP 200 with status ok.

    Public endpoint — no authentication required, no secrets exposed, read-only.
    """
    return {"status": "ok"}


@app.get("/greet/{name}")
def greet(
    name: Annotated[str, Path(max_length=64, description="Name to greet (max 64 characters)")],
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
