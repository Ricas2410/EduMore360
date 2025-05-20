FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install minimal dependencies
RUN pip install --upgrade pip && \
    pip install gunicorn

# Copy only the minimal application
COPY railway_app.py /app/

# Run as non-root user
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Run gunicorn with the minimal application
CMD gunicorn railway_app:application --bind 0.0.0.0:$PORT --log-level debug --workers 1 --timeout 120
