"""
FastAPI greeting web service.

Access control note: all endpoints are public and read-only, hold no secrets,
and perform no writes. Authentication / authorisation is explicitly out of scope.
"""

from typing import Annotated

from fastapi import FastAPI, Path

# Access control: no auth middleware — all endpoints intentionally public.
app = FastAPI(title="hello-python", version="0.1.0")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Health-check endpoint — always returns HTTP 200."""
    return {"status": "ok"}


@app.get("/greet/{name}")
async def greet(name: Annotated[str, Path(max_length=64)]) -> dict[str, str]:
    """Return a personalised greeting for *name*.

    Access control: public, read-only, no secrets, no writes.
    """
    return {"message": f"Hello, {name}!"}


def main() -> None:
    """Entry-point for uvicorn via the CLI script."""
    import uvicorn

    uvicorn.run("hello_python.web:app", host="0.0.0.0", port=8080, reload=False)


if __name__ == "__main__":
    main()
