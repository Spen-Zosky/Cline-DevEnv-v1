FROM python:3.12-alpine@sha256:c08bfdbffc9184cdfd225497bac12b2c0dac1d24bbe13287cfb7d99f1116cf43

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    curl \
    gcc \
    musl-dev

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8082

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8082/health || exit 1

# Start the application
CMD ["python", "src/main.py"]
