# Stage 1: Build environment
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies for Debian
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.12-slim

WORKDIR /app

# Install NGINX
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app/ ./app/

# Copy NGINX configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Ensure PATH includes local binaries
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 80

# Start NGINX and Gunicorn
CMD ["/start.sh"]
