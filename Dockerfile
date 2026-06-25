# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifest first for layer-cache efficiency
COPY pyproject.toml ./

# Copy application source
COPY src/ ./src/

# Create a virtual environment and install the package with its dependencies
ENV VIRTUAL_ENV=/app/.venv
RUN uv venv .venv && uv pip install --no-cache .

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy only the virtual environment (contains installed packages)
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    VIRTUAL_ENV=/app/.venv \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8080

# Access control: all endpoints are public, read-only, no secrets, no writes.
CMD ["uvicorn", "hello_python.web:app", "--host", "0.0.0.0", "--port", "8080"]
