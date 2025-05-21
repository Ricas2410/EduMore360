"""
Render-specific settings for edumore360 project.
This file is used when deploying to Render.
"""

import os
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .settings import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

# Allow Render domains and any custom domains
ALLOWED_HOSTS = ['*', '.onrender.com']

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://edumore360.onrender.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Security settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Add CORS headers
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
STATIC_ROOT = '/app/staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add whitenoise middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Database configuration - use dj_database_url to parse the DATABASE_URL
# This is more flexible and will work with Render's database provisioning
db_url = os.environ.get('DATABASE_URL')
if db_url:
    DATABASES['default'] = dj_database_url.parse(db_url, conn_max_age=600, ssl_require=True)
    print(f"Using database: {DATABASES['default']['NAME']} on {DATABASES['default']['HOST']}")
else:
    print("WARNING: DATABASE_URL not set. Using default database configuration.")

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
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='')

# Media files - use Wasabi Cloud Storage in production
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Wasabi credentials from environment variables
AWS_ACCESS_KEY_ID = env('WASABI_ACCESS_KEY', default='')
AWS_SECRET_ACCESS_KEY = env('WASABI_SECRET_KEY', default='')
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

# Logging - simplified for Render deployment
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
