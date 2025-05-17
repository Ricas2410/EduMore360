#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env.production

# Print deployment info
echo "Deploying EduMore360 to production..."
echo "Environment: Production"
echo "Settings module: $DJANGO_SETTINGS_MODULE"

# Pull latest changes
echo "Pulling latest changes from repository..."
git pull

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Build static assets
echo "Building static assets..."
cd theme/static_src
npm install
npm run build
cd ../..

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Restart services
echo "Restarting services..."
if [ -f /etc/systemd/system/gunicorn-edumore360.service ]; then
    sudo systemctl restart gunicorn-edumore360
fi

if [ -f /etc/systemd/system/celery-edumore360.service ]; then
    sudo systemctl restart celery-edumore360
fi

if [ -f /etc/systemd/system/celerybeat-edumore360.service ]; then
    sudo systemctl restart celerybeat-edumore360
fi

# Reload Nginx
echo "Reloading Nginx..."
sudo systemctl reload nginx

echo "Deployment completed successfully!"
