
import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
# Read .env file explicitly
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='5#e98z!#hxs)ms55c+yw0!r-+q3w$4p=yz7w!0b13^d=e@bx)1')

DEBUG = env.bool('DEBUG', default=False)

# Set allowed hosts from environment variable
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Security settings for production
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # Disable SSL redirect in development
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

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
    'user_agents',  # For analytics user agent parsing

    # Local apps
    'accounts.apps.AccountsConfig',
    'core.apps.CoreConfig',
    'curriculum.apps.CurriculumConfig',
    'quiz.apps.QuizConfig',
    'subscription.apps.SubscriptionConfig',
    'search.apps.SearchConfig',
    'theme.apps.ThemeConfig',
    'my_admin.apps.MyAdminConfig',
    'analytics.apps.AnalyticsConfig',  # Analytics app
    'healthcheck',
    'minimal_health',  # Minimal health check app
]

# Tailwind configuration
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Site ID for django-allauth
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'subscription.middleware.SubscriptionMiddleware',  # Subscription restrictions
    # 'analytics.middleware.AnalyticsMiddleware',  # Analytics tracking - DISABLED for memory optimization
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
                'core.context_processors.notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'edumore360.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Database configuration
# Priority: 1. DATABASE_URL environment variable, 2. DATABASE_URL in .env, 3. SQLite
import dj_database_url

# Get DATABASE_URL from environment or .env file
db_url = os.environ.get('DATABASE_URL', env('DATABASE_URL', default=None))

# IMPORTANT: For Render deployment, we need to be more flexible
# If we're on Render, we'll use a hardcoded Neon PostgreSQL URL
if os.environ.get('RENDER', False):
    print("Running on Render, using hardcoded Neon PostgreSQL URL")
    db_url = "postgresql://neondb_owner:npg_R5dEIG2wvtSl@ep-soft-violet-a58sv217-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
# For development or other environments, we can be more flexible
elif not db_url:
    print("WARNING: DATABASE_URL is not set. Using SQLite as a fallback.")
    db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
elif not db_url.startswith('postgresql'):
    print(f"WARNING: DATABASE_URL does not start with 'postgresql': {db_url}")
    print("This may cause issues in production environments.")

# Use PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=db_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
}
print(f"Using PostgreSQL database: {DATABASES['default']['NAME']} on {DATABASES['default']['HOST']}")

# Memory optimization for production
if not DEBUG:
    # Limit database connections to prevent memory issues
    DATABASES['default']['CONN_MAX_AGE'] = 300  # 5 minutes
    DATABASES['default']['OPTIONS'] = {
        'MAX_CONNS': 10,  # Limit max connections
        'MIN_CONNS': 2,   # Minimum connections
    }

# Add SQLite as a secondary connection for data migration scripts
if 'default' in DATABASES and DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
    DATABASES['sqlite'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (overridden by B2 settings below if enabled)


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Django AllAuth settings
ACCOUNT_LOGIN_METHODS = ['email']
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGIN_URL = 'account_login'

# Disable HTTPS for AllAuth in development
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https' if not DEBUG else 'http'

# Email settings for AllAuth
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""  # Remove the default [site name] prefix
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # Links expire after 1 day
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'core:dashboard'  # Redirect to dashboard after confirmation
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'account_login'  # Redirect to login if not authenticated
ACCOUNT_EMAIL_HTML = True  # Enable HTML emails

# Rate limiting settings for AllAuth
ACCOUNT_RATE_LIMITS = {
    # 3 minutes cooldown between confirmation emails
    "confirm_email": "180/h",
}

# Use custom adapter for AllAuth
ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

# Custom forms
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
    'login': 'accounts.forms.CustomLoginForm',
}

# Email settings - Using SMTP for both development and production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='skillnetservices@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='tdms ckdk tmgo fado')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='skillnetservices@gmail.com')

# Fallback to console backend if SMTP credentials are not provided
if not (EMAIL_HOST_USER and EMAIL_HOST_PASSWORD) and DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("WARNING: Email credentials not provided. Using console backend for emails.")

# Cache settings
# Use Redis in production, but use local memory cache for development
REDIS_URL = env('REDIS_URL', default=None)
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# Celery settings
# Use Redis in production, but use Django database for development
if REDIS_URL:
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
else:
    CELERY_BROKER_URL = 'django://'
    CELERY_RESULT_BACKEND = 'django-db'
    INSTALLED_APPS += ['django_celery_results']

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Summernote settings
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'width': '100%',
        'height': '300px',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    },
    'attachment_absolute_uri': True,
}

# Summernote theme
SUMMERNOTE_THEME = 'bs4'  # Use Bootstrap 4 theme

# Paystack settings
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY', default='sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY', default='pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# Currency conversion settings
USD_TO_GHS_RATE = env.float('USD_TO_GHS_RATE', default=13.5)

# Wasabi Cloud Storage Settings
# Use Wasabi for media storage in both development and production
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

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development
CORS_ALLOWED_ORIGINS = [
    "https://edumore360.up.railway.app",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
