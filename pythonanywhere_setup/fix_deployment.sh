#!/bin/bash

# 🔧 EduMore360 PythonAnywhere Deployment Fix Script
# Run this script to fix common deployment issues

echo "🔧 Fixing EduMore360 deployment issues..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "manage.py not found. Please run this script from the EduMore360 root directory."
    exit 1
fi

print_status "Starting deployment fixes..."

# Activate virtual environment
source venv/bin/activate

# Fix 1: Remove Celery dependency
print_status "Removing Celery dependency..."
cat > edumore360/__init__.py << 'EOF'
# Django app initialization
# Celery removed for PythonAnywhere compatibility
EOF

# Fix 2: Install missing dependencies
print_status "Installing missing dependencies..."
pip install python-decouple

# Fix 3: Update settings to use PythonAnywhere configuration
print_status "Setting up PythonAnywhere settings..."
export DJANGO_SETTINGS_MODULE=edumore360.settings_pythonanywhere

# Fix 4: Copy environment file with your existing configuration
print_status "Setting up environment file..."
cat > .env << 'EOF'
# EduMore360 PythonAnywhere Environment Variables
DEBUG=False
SECRET_KEY=5#e98z!#hxs)ms55c+yw0!r-+q3w$4p=yz7w!0b13^d=e@bx)1
ALLOWED_HOSTS=localhost,127.0.0.1,edumore360.pythonanywhere.com

# Wasabi Cloud Storage (your existing configuration)
WASABI_ACCESS_KEY=RD7YA4Z2P3LF7E4JEZUO
WASABI_SECRET_KEY=QY8JXIshozz5J6CU3AzBCvyArDqXtd13wNEyMho7
WASABI_BUCKET_NAME=edumore360-media
WASABI_REGION=us-east-1

# Email settings (your existing configuration)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=skillnetservices@gmail.com
EMAIL_HOST_PASSWORD=tdms ckdk tmgo fado
DEFAULT_FROM_EMAIL=skillnetservices@gmail.com

# Paystack settings (your existing configuration)
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PAYSTACK_PUBLIC_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Currency conversion rate
USD_TO_GHS_RATE=14.5

# Performance Settings
CACHE_TIMEOUT=300
SESSION_COOKIE_AGE=86400
ANALYTICS_ENABLED=False
MAX_UPLOAD_SIZE=5242880
EOF

# Fix 5: Run database migrations
print_status "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Fix 6: Create cache table
print_status "Creating cache table..."
python manage.py createcachetable

# Fix 7: Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Fix 8: Create admin user if it doesn't exist
print_status "Setting up admin user..."
python -c "
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@edumore360.com').exists():
    User.objects.create_superuser(
        email='admin@edumore360.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Admin user created successfully')
else:
    print('Admin user already exists')
"

# Fix 9: Set up basic curriculum data
print_status "Setting up basic curriculum..."
python pythonanywhere_setup/migrate_and_setup.py

print_status "All fixes applied successfully!"

echo ""
echo "🎉 Deployment fixes completed!"
echo "================================"
echo ""
echo "📋 Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Set virtualenv path to: /home/edumore360/EduMore360/venv"
echo "3. Make sure WSGI file contains the correct configuration"
echo "4. Set static files mapping: /static/ -> /home/edumore360/EduMore360/staticfiles/"
echo "5. Reload your web app"
echo ""
echo "🔐 Admin login:"
echo "URL: https://edumore360.pythonanywhere.com/my-admin/"
echo "Email: admin@edumore360.com"
echo "Password: admin123"
echo ""
echo "✅ Your EduMore360 platform should now work perfectly!"

deactivate
