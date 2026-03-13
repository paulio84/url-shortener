# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim AS production

WORKDIR /app

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY wsgi.py ./
COPY entrypoint.sh ./

# Change the permission to execute the entrypoint.sh script
RUN chmod +x entrypoint.sh

# Ensure the venv binaries take precedence
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=wsgi:flask_app

# Switch to the non-root user
USER appuser

EXPOSE 8000

# Use gunicorn as the production WSGI server
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "wsgi:flask_app"]
