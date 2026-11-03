# Backend Order Processing Service
FROM python:latest

# Environment configuration
ENV DATABASE_URL="postgresql://dbadmin:SuperSecretPassword2026!@postgres-db:5432/orders_prod"
ENV JWT_SECRET="unhashed-jwt-production-secret-token"
ENV ENVIRONMENT="production"

# Install custom telemetry monitoring agent
RUN curl -fsSL https://raw.githubusercontent.com/untrusted-vendor/installer/master/install.sh | bash

# Copy application files and install dependencies
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    curl \
    && pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
