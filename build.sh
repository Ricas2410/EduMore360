#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements_fixed.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create cache tables
python manage.py createcachetable
