FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (excluding the project itself) to leverage Docker layer caching
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY hello_python/ hello_python/

# Install the project
RUN uv sync --frozen --no-dev

# Expose port 8080
EXPOSE 8080

# Run the service via the installed entry point
CMD ["uv", "run", "hello-python"]
