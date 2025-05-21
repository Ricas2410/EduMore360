"""
Direct settings file for Render deployment.
This file has hardcoded values and doesn't rely on environment variables.
"""

import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
# Read .env file explicitly
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-key-for-render-deployment-only'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow Render domains and any custom domains
ALLOWED_HOSTS = ['*', '.onrender.com']

# Application definition
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'crispy_tailwind',
    'django_summernote',
    'django_htmx',
    'tailwind',
    'storages',
    'corsheaders',

    # Local apps
    'accounts.apps.AccountsConfig',
    'core.apps.CoreConfig',
    'curriculum.apps.CurriculumConfig',
    'quiz.apps.QuizConfig',
    'subscription.apps.SubscriptionConfig',
    'search.apps.SearchConfig',
    'theme.apps.ThemeConfig',
    'my_admin.apps.MyAdminConfig',
    'healthcheck',
    'minimal_health',  # Minimal health check app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add CORS headers
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',  # Add HTMX middleware
]

ROOT_URLCONF = 'edumore360.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'edumore360.wsgi.application'

# Database - hardcoded for Render deployment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_R5dEIG2wvtSl',
        'HOST': 'ep-soft-violet-a58sv217-pooler.us-east-2.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Add SQLite as a secondary connection for data migration scripts
DATABASES['sqlite'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Site ID for django.contrib.sites
SITE_ID = 1

# Django AllAuth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# Login/logout URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Crispy Forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

# Tailwind settings
TAILWIND_APP_NAME = 'theme'

# Email settings - hardcoded for Render deployment
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'skillnetservices@gmail.com'
EMAIL_HOST_PASSWORD = 'tdms ckdk tmgo fado'
DEFAULT_FROM_EMAIL = 'skillnetservices@gmail.com'

# Wasabi Cloud Storage Settings - hardcoded for Render deployment
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'RD7YA4Z2P3LF7E4JEZUO'
AWS_SECRET_ACCESS_KEY = 'QY8JXIshozz5J6CU3AzBCvyArDqXtd13wNEyMho7'
AWS_STORAGE_BUCKET_NAME = 'edumore360-media'
AWS_S3_REGION_NAME = 'us-east-1'

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

# Summernote theme
SUMMERNOTE_THEME = 'bs4'  # Use Bootstrap 4 theme

# Paystack settings
PAYSTACK_SECRET_KEY = 'sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
PAYSTACK_PUBLIC_KEY = 'pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Currency conversion settings
USD_TO_GHS_RATE = 14.5

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
SECURE_SSL_REDIRECT = False  # Set to False for Render
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging configuration
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
