"""
Production settings for EduMore360 on PythonAnywhere
Optimized for performance and security
"""

from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-this')

# Allowed hosts for PythonAnywhere
ALLOWED_HOSTS = [
    'yourusername.pythonanywhere.com',  # Replace with your PythonAnywhere username
    'edumore360.com',  # Replace with your custom domain
    'www.edumore360.com',
    'localhost',
    '127.0.0.1',
]

# Database configuration for PythonAnywhere MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'yourusername$edumore360'),  # Replace with your database name
        'USER': os.environ.get('DB_USER', 'yourusername'),  # Replace with your username
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your-mysql-password'),  # Set your MySQL password
        'HOST': os.environ.get('DB_HOST', 'yourusername.mysql.pythonanywhere-services.com'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Email configuration (optional - for production emails)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@edumore360.com')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache configuration (optional - for better performance)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutes
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Performance optimizations
USE_TZ = True
USE_I18N = True
USE_L10N = True

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Admin media prefix
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Disable analytics middleware in production for better performance
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'subscription.middleware.SubscriptionMiddleware',
    # Analytics middleware disabled for performance
    # 'analytics.middleware.AnalyticsMiddleware',
]

# Paystack settings (for payments)
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY', '')
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY', '')

# Wasabi storage settings (if using for media files)
USE_WASABI = os.environ.get('USE_WASABI', 'False').lower() == 'true'

if USE_WASABI:
    # Wasabi S3 settings
    AWS_ACCESS_KEY_ID = os.environ.get('WASABI_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('WASABI_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('WASABI_BUCKET_NAME', '')
    AWS_S3_ENDPOINT_URL = 'https://s3.wasabisys.com'
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.wasabisys.com'
    
    # Media files storage
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Django Allauth settings
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Site ID for Django sites framework
SITE_ID = 1

# Time zone
TIME_ZONE = 'UTC'

# Language code
LANGUAGE_CODE = 'en-us'

# Performance: Disable migrations in production (optional)
# MIGRATION_MODULES = {app: None for app in INSTALLED_APPS}

print("✅ Production settings loaded for PythonAnywhere")
print(f"📊 Database: MySQL on {DATABASES['default']['HOST']}")
print(f"🌐 Allowed hosts: {ALLOWED_HOSTS}")
print(f"📁 Static files: {STATIC_ROOT}")
print(f"🔒 Debug mode: {DEBUG}")
