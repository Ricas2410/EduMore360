#!/usr/bin/env bash
# exit on error
set -o errexit

# Set the RENDER environment variable
export RENDER=true

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements_fixed.txt

# Patch the settings file to be more flexible with database URLs
echo "Patching settings file for Render compatibility..."
python patch_settings.py || echo "Settings patch failed, but continuing..."

# Set up the database configuration
echo "Setting up database configuration..."
python render_db_setup.py || echo "Database setup failed, but continuing..."

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
