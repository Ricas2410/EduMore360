#!/usr/bin/env bash
# exit on error
set -o errexit

# Set the RENDER environment variable
export RENDER=true

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements_fixed.txt

# Use direct settings for Render deployment
echo "Using direct settings for Render deployment..."
export DJANGO_SETTINGS_MODULE=edumore360.settings_direct

# Print environment variables for debugging (without sensitive values)
echo "Environment variables:"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DEBUG: $DEBUG"
echo "RENDER: $RENDER"
echo "DATABASE_URL is set: $(if [ -n "$DATABASE_URL" ]; then echo "Yes"; else echo "No"; fi)"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input || echo "Static file collection failed, but continuing..."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate || echo "Database migration failed, but continuing..."

# Create cache tables
echo "Creating cache tables..."
python manage.py createcachetable || echo "Cache table creation failed, but continuing..."

echo "Build process completed."
