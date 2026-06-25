"""
FastAPI greeting web service.

Access control note: all endpoints are public and read-only, hold no secrets,
and perform no writes — access control is explicitly out of scope for this service.
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="hello-python", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Health check endpoint. Returns HTTP 200 with status ok."""
    return {"status": "ok"}


def main() -> None:
    uvicorn.run("hello_python.web:app", host="0.0.0.0", port=8080, reload=False)


if __name__ == "__main__":
    main()
