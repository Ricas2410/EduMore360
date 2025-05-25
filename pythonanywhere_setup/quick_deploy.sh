#!/bin/bash

# 🚀 EduMore360 Quick Deployment Script for PythonAnywhere
# This script performs a complete fresh deployment

echo "🚀 EduMore360 Quick Deployment for PythonAnywhere"
echo "=================================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# Check if running on PythonAnywhere
if [[ ! "$PWD" =~ ^/home/[^/]+/?$ ]]; then
    print_warning "This script is designed for PythonAnywhere. Current directory: $PWD"
fi

print_step "1. Cleaning up existing installation..."

# Remove existing directory
if [ -d "EduMore360" ]; then
    rm -rf EduMore360
    print_status "Removed existing EduMore360 directory"
fi

print_step "2. Cloning repository..."

# Clone the repository
git clone https://github.com/Ricas2410/EduMore360.git

if [ $? -ne 0 ]; then
    print_error "Failed to clone repository"
    exit 1
fi

cd EduMore360
print_status "Repository cloned successfully"

print_step "3. Setting up virtual environment..."

# Create and activate virtual environment
python3.10 -m venv venv
source venv/bin/activate

if [ $? -ne 0 ]; then
    print_error "Failed to create virtual environment"
    exit 1
fi

print_status "Virtual environment created"

print_step "4. Installing dependencies..."

# Install requirements
pip install --upgrade pip
pip install -r pythonanywhere_setup/requirements_pythonanywhere.txt

if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies"
    exit 1
fi

print_status "Dependencies installed"

print_step "5. Setting up configuration files..."

# Copy configuration files
cp pythonanywhere_setup/pythonanywhere_settings.py edumore360/settings_pythonanywhere.py
cp pythonanywhere_setup/pythonanywhere_wsgi.py wsgi_pythonanywhere.py
cp pythonanywhere_setup/pythonanywhere.env .env

# Update .gitignore
cat pythonanywhere_setup/update_gitignore.txt >> .gitignore

print_status "Configuration files set up"

print_step "6. Setting up static files..."

# Create static directories
mkdir -p staticfiles static/css static/js static/images

# Set Django settings
export DJANGO_SETTINGS_MODULE=edumore360.settings_pythonanywhere

# Collect static files
python manage.py collectstatic --noinput

print_status "Static files configured"

print_step "7. Setting up database..."

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create cache table
python manage.py createcachetable

print_status "Database set up"

print_step "8. Creating admin user and sample data..."

# Run setup script
python pythonanywhere_setup/migrate_and_setup.py

print_status "Admin user and sample data created"

print_step "9. Final configuration..."

# Create media directories
mkdir -p media/uploads media/profile_pictures media/quiz_images media/notes

print_status "Media directories created"

# Deactivate virtual environment
deactivate

echo ""
echo "🎉 Deployment completed successfully!"
echo "====================================="
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your actual credentials:"
echo "   - SECRET_KEY (generate new one)"
echo "   - WASABI_ACCESS_KEY_ID"
echo "   - WASABI_SECRET_ACCESS_KEY"
echo "   - WASABI_STORAGE_BUCKET_NAME"
echo "   - Email settings (optional)"
echo ""
echo "2. Go to PythonAnywhere Web tab and:"
echo "   - Create new web app (Python 3.10, Manual configuration)"
echo "   - Set source code: /home/$(whoami)/EduMore360"
echo "   - Set working directory: /home/$(whoami)/EduMore360"
echo "   - Copy content from wsgi_pythonanywhere.py to WSGI file"
echo ""
echo "3. Configure static files in Web tab:"
echo "   URL: /static/"
echo "   Directory: /home/$(whoami)/EduMore360/staticfiles/"
echo ""
echo "4. Configure media files in Web tab:"
echo "   URL: /media/"
echo "   Directory: /home/$(whoami)/EduMore360/media/"
echo ""
echo "5. Reload your web app"
echo ""
echo "🔐 Admin credentials:"
echo "Email: admin@edumore360.com"
echo "Password: admin123"
echo "⚠️  Change password after first login!"
echo ""
echo "🌟 Your EduMore360 platform is ready!"
echo "Visit: https://$(whoami).pythonanywhere.com"

# Final check
if [ -f ".env" ] && [ -f "manage.py" ] && [ -d "venv" ]; then
    print_status "All files are in place"
    echo ""
    echo "✅ Deployment verification passed!"
else
    print_error "Some files are missing. Please check the deployment."
    exit 1
fi
