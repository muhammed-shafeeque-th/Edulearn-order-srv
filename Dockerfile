###############################################
# Stage 1: Builder
###############################################
FROM python:3.11-alpine AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies (CRITICAL)
RUN apk add --no-cache \
    build-base \
    linux-headers \
    python3-dev \
    zlib-dev \
    curl

# Copy dependency file
COPY requirements.txt .

# Upgrade pip (important for pyproject builds)
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .
###############################################
# Stage 2: Runtime
###############################################
FROM python:3.11-alpine AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Runtime-only deps (NO compilers)
RUN apk add --no-cache \
    zlib \
    curl \
    netcat-openbsd

# Copy Python packages from builder
COPY --from=builder /usr/local /usr/local

# Copy app source
COPY . .

# Security: non-root user
RUN adduser -D appuser
USER appuser

# Ports
EXPOSE 8000 50051

# Start service
CMD ["python", "src/main.py"]
