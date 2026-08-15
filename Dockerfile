# Build stage ─
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies (needed by some C-extension packages, e.g. asyncpg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage 
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.title="DevMate"
LABEL org.opencontainers.image.description="AI-powered Discord developer-community bot"

# Non-root user for security
RUN useradd --create-home --shell /bin/bash devmate

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source (secrets are passed at runtime via env vars, not baked in)
COPY --chown=devmate:devmate . .

USER devmate

# Unbuffered output so logs appear immediately in `docker compose logs`
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "main.py"]
