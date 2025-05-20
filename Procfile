web: gunicorn hybrid_app:application --env DJANGO_SETTINGS_MODULE=edumore360.settings_prod --log-level debug --timeout 120 --workers 1
worker: celery -A edumore360 worker --loglevel=info
