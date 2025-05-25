#!/bin/bash

# 📁 EduMore360 Static Files Setup for PythonAnywhere
# This script configures static files for optimal performance

echo "📁 Setting up static files for PythonAnywhere..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ manage.py not found. Please run this script from the EduMore360 root directory."
    exit 1
fi

print_step "1. Creating static directories..."

# Create static file directories
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images
mkdir -p static/fonts
mkdir -p static/admin
mkdir -p staticfiles

print_status "Static directories created"

print_step "2. Setting up CSS files..."

# Create main CSS file if it doesn't exist
if [ ! -f "static/css/main.css" ]; then
    cat > static/css/main.css << 'EOF'
/* EduMore360 Main Styles */
:root {
    --primary-color: #4e73df;
    --secondary-color: #224abe;
    --success-color: #1cc88a;
    --info-color: #36b9cc;
    --warning-color: #f6c23e;
    --danger-color: #e74a3b;
    --light-color: #f8f9fc;
    --dark-color: #5a5c69;
}

body {
    font-family: 'Nunito', sans-serif;
    background-color: var(--light-color);
}

.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.btn-primary:hover {
    background-color: var(--secondary-color);
    border-color: var(--secondary-color);
}

.text-primary {
    color: var(--primary-color) !important;
}

/* Responsive utilities */
@media (max-width: 768px) {
    .container-fluid {
        padding: 0.5rem;
    }
}
EOF
    print_status "Created main.css"
fi

print_step "3. Setting up JavaScript files..."

# Create main JS file if it doesn't exist
if [ ! -f "static/js/main.js" ]; then
    cat > static/js/main.js << 'EOF'
// EduMore360 Main JavaScript

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Utility functions
function showLoading(element) {
    element.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

// CSRF token helper
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
EOF
    print_status "Created main.js"
fi

print_step "4. Setting up favicon..."

# Create a simple favicon placeholder
if [ ! -f "static/images/favicon.ico" ]; then
    # Create a simple text file as placeholder
    echo "Favicon placeholder - replace with actual favicon.ico" > static/images/favicon.ico
    print_status "Created favicon placeholder"
fi

print_step "5. Collecting static files..."

# Set Django settings module
export DJANGO_SETTINGS_MODULE=edumore360.settings_pythonanywhere

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Collect static files
python manage.py collectstatic --noinput --clear

print_status "Static files collected successfully"

print_step "6. Setting up media directories..."

# Create media directories (even though we use Wasabi)
mkdir -p media/uploads
mkdir -p media/profile_pictures
mkdir -p media/quiz_images
mkdir -p media/notes

print_status "Media directories created"

print_step "7. Creating .htaccess for static files (if needed)..."

# Create .htaccess for better caching
cat > staticfiles/.htaccess << 'EOF'
# Static files caching
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/gif "access plus 1 month"
    ExpiresByType image/svg+xml "access plus 1 month"
    ExpiresByType font/woff "access plus 1 month"
    ExpiresByType font/woff2 "access plus 1 month"
</IfModule>

# Compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>
EOF

print_status "Created .htaccess for static files"

echo ""
echo "🎉 Static files setup completed!"
echo ""
echo "📋 PythonAnywhere Web App Configuration:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Set static files mapping:"
echo "   URL: /static/"
echo "   Directory: /home/edumore360/EduMore360/staticfiles/"
echo ""
echo "3. Set media files mapping:"
echo "   URL: /media/"
echo "   Directory: /home/edumore360/EduMore360/media/"
echo ""
echo "4. Optional: Enable HTTPS in PythonAnywhere settings"
echo ""
echo "🌟 Your static files are ready for production!"

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi
