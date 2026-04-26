# Full-stack Dockerfile for Na Rejonie application
# Backend: Django + MySQL
# Frontend: Static HTML/CSS/JS served by Django

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies for MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy backend code
COPY backend/ /app/

# Copy frontend code
COPY frontend/ /app/frontend/

# Create directories for static and media files
RUN mkdir -p /app/static /app/media

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Set proper permissions
RUN chmod +x manage.py

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
