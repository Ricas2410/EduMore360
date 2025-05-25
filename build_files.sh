#!/bin/bash

# Build script for Vercel deployment
echo "Building EduMore360 for Vercel..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

echo "Build complete!"
