"""
Production settings for edumore360 project.
"""

import os  # Used for path operations and environment variables
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .settings import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Temporarily enabled for troubleshooting

# Allow all Railway domains and any custom domains
ALLOWED_HOSTS = ['*', '.up.railway.app', '.railway.app']

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development
CORS_ALLOWED_ORIGINS = [
    "https://edumore360.up.railway.app",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Security settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = False  # Temporarily disabled for troubleshooting
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Add CORS headers
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_CREDENTIALS = True

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https://via.placeholder.com")
CSP_CONNECT_SRC = ("'self'",)

# Permissions Policy
PERMISSIONS_POLICY = {
    'accelerometer': [],
    'camera': [],
    'geolocation': [],
    'gyroscope': [],
    'magnetometer': [],
    'microphone': [],
    'payment': ['self'],
    'usb': [],
}

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add whitenoise middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Add security middleware
# Make sure we don't add duplicates
security_middleware = [
    'django.middleware.security.SecurityMiddleware',
]

# Only add middleware that's not already in the list and is available
for middleware in security_middleware:
    if middleware not in MIDDLEWARE:
        MIDDLEWARE.append(middleware)

# Try to add optional middleware if available
try:
    import csp
    if 'csp.middleware.CSPMiddleware' not in MIDDLEWARE:
        MIDDLEWARE.append('csp.middleware.CSPMiddleware')
except ImportError:
    pass

try:
    import django_permissions_policy
    if 'django_permissions_policy.PermissionsPolicyMiddleware' not in MIDDLEWARE:
        MIDDLEWARE.append('django_permissions_policy.PermissionsPolicyMiddleware')
except ImportError:
    pass

try:
    import corsheaders
    if 'corsheaders.middleware.CorsMiddleware' not in MIDDLEWARE:
        # Insert CORS middleware in the correct position (after SessionMiddleware, before CommonMiddleware)
        session_index = MIDDLEWARE.index('django.contrib.sessions.middleware.SessionMiddleware')
        MIDDLEWARE.insert(session_index + 1, 'corsheaders.middleware.CorsMiddleware')
except (ImportError, ValueError):
    pass

# Database - use PostgreSQL in production
# We're using the same database configuration as in settings.py
# This ensures we use the same database in both local and production environments
# The configuration is already set in settings.py, which we import at the top of this file

# Add some production-specific database settings
if 'default' in DATABASES:
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['ATOMIC_REQUESTS'] = True

# Cache - use Redis in production if available, otherwise use local memory cache
REDIS_URL = env('REDIS_URL', default=None)
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'KEY_PREFIX': 'edumore360',
            'TIMEOUT': 300,  # 5 minutes
        }
    }

    # Celery settings with Redis
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_ALWAYS_EAGER = False
    CELERY_TASK_EAGER_PROPAGATES = False
else:
    # Fallback to local memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'edumore360',
        }
    }

    # Celery settings without Redis
    CELERY_BROKER_URL = 'django://'
    CELERY_RESULT_BACKEND = 'django-db'
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    # Only add django_celery_results if it's not already in INSTALLED_APPS
    if 'django_celery_results' not in INSTALLED_APPS:
        INSTALLED_APPS += ['django_celery_results']

# Email settings - use SMTP in production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='skillnetservices@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='tdms ckdk tmgo fado')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='skillnetservices@gmail.com')

# Media files - use Wasabi Cloud Storage in production
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Wasabi credentials from environment variables
AWS_ACCESS_KEY_ID = env('WASABI_ACCESS_KEY', default='RD7YA4Z2P3LF7E4JEZUO')
AWS_SECRET_ACCESS_KEY = env('WASABI_SECRET_KEY', default='QY8JXIshozz5J6CU3AzBCvyArDqXtd13wNEyMho7')
AWS_STORAGE_BUCKET_NAME = env('WASABI_BUCKET_NAME', default='edumore360-media')
AWS_S3_REGION_NAME = env('WASABI_REGION', default='us-east-1')

# Wasabi specific settings
AWS_S3_ENDPOINT_URL = f'https://s3.{AWS_S3_REGION_NAME}.wasabisys.com'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'private'  # Use private ACL since public access is not allowed
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = True  # Enable query string auth for private files
AWS_QUERYSTRING_EXPIRE = 86400  # URLs expire after 24 hours (86400 seconds)

# Media files URL - Wasabi format
MEDIA_URL = f'https://s3.{AWS_S3_REGION_NAME}.wasabisys.com/{AWS_STORAGE_BUCKET_NAME}/'

# Sentry for error tracking
SENTRY_DSN = env('SENTRY_DSN', default=None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True,
    )

# Logging - simplified for Railway deployment
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'edumore360': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
