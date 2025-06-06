# Backend-only Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  g++ \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r ultimon && useradd -r -g ultimon ultimon

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./server/

# Copy LibreHardwareMonitor DLL from root
COPY LibreHardwareMonitorLib.dll ./LibreHardwareMonitorLib.dll

# Create necessary directories
RUN mkdir -p /app/data /app/logs && \
  chown -R ultimon:ultimon /app/data /app/logs

# Switch to non-root user
USER ultimon

# Expose port
EXPOSE 8100

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8100/health || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "server.app.main:app", "--host", "0.0.0.0", "--port", "8100"]
