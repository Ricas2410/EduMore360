#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements_fixed.txt

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
