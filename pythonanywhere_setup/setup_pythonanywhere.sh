#!/bin/bash

# 🚀 EduMore360 PythonAnywhere Setup Script
# This script sets up the complete EduMore360 environment on PythonAnywhere

echo "🚀 Starting EduMore360 PythonAnywhere Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "manage.py not found. Please run this script from the EduMore360 root directory."
    exit 1
fi

print_step "1. Setting up Python virtual environment..."

# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

print_status "Virtual environment created and activated"

print_step "2. Installing Python dependencies..."

# Copy requirements file
cp pythonanywhere_setup/requirements_pythonanywhere.txt requirements.txt

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

print_status "Dependencies installed successfully"

print_step "3. Setting up environment variables..."

# Copy environment file
cp pythonanywhere_setup/pythonanywhere.env .env

print_warning "Please edit .env file with your actual values before proceeding!"
print_warning "Update the following in .env:"
echo "  - SECRET_KEY"
echo "  - WASABI_ACCESS_KEY_ID"
echo "  - WASABI_SECRET_ACCESS_KEY"
echo "  - WASABI_STORAGE_BUCKET_NAME"
echo "  - EMAIL settings (if needed)"
echo "  - PAYSTACK keys (if needed)"

print_step "4. Setting up Django settings..."

# Copy PythonAnywhere settings
cp pythonanywhere_setup/pythonanywhere_settings.py edumore360/settings_pythonanywhere.py

print_status "Django settings configured for PythonAnywhere"

print_step "5. Setting up WSGI configuration..."

# Copy WSGI file
cp pythonanywhere_setup/pythonanywhere_wsgi.py wsgi_pythonanywhere.py

print_status "WSGI configuration ready"

print_step "6. Updating .gitignore..."

# Update .gitignore
cat pythonanywhere_setup/update_gitignore.txt >> .gitignore

print_status ".gitignore updated"

print_step "7. Setting up static files directories..."

# Create static directories
mkdir -p staticfiles
mkdir -p static/admin
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images

print_status "Static directories created"

print_step "8. Collecting static files..."

# Set Django settings module
export DJANGO_SETTINGS_MODULE=edumore360.settings_pythonanywhere

# Collect static files
python manage.py collectstatic --noinput

print_status "Static files collected"

print_step "9. Setting up database..."

# Run migrations
python manage.py makemigrations
python manage.py migrate

print_status "Database migrations completed"

print_step "10. Creating cache table..."

# Create cache table for better performance
python manage.py createcachetable

print_status "Cache table created"

print_step "11. Final setup tasks..."

# Run the final setup script
python pythonanywhere_setup/migrate_and_setup.py

print_status "Final setup completed"

echo ""
echo "🎉 EduMore360 setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your actual values"
echo "2. Go to PythonAnywhere Web tab"
echo "3. Create a new web app (Python 3.10, Manual configuration)"
echo "4. Set source code directory to: /home/edumore360/EduMore360"
echo "5. Set working directory to: /home/edumore360/EduMore360"
echo "6. Update WSGI file with content from wsgi_pythonanywhere.py"
echo "7. Set static files mapping:"
echo "   URL: /static/"
echo "   Directory: /home/edumore360/EduMore360/staticfiles/"
echo "8. Set media files mapping:"
echo "   URL: /media/"
echo "   Directory: /home/edumore360/EduMore360/media/"
echo "9. Reload your web app"
echo ""
echo "🌟 Your EduMore360 platform will be ready!"

# Deactivate virtual environment
deactivate

print_status "Setup script completed. Please follow the next steps above."
