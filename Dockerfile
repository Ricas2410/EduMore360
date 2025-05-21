FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE edumore360.settings_prod

# Set work directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_fixed.txt /app/requirements_fixed.txt
RUN pip install --upgrade pip && \
    pip install -r requirements_fixed.txt

# Copy the hybrid application first (for health checks)
COPY hybrid_app.py /app/

# Copy the rest of the project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput || echo "Collectstatic failed, but continuing"

# Run as non-root user
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Run gunicorn with the hybrid application
CMD gunicorn hybrid_app:application --bind 0.0.0.0:$PORT --log-level debug --workers 1 --timeout 120
