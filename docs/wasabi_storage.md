# Using Wasabi Cloud Storage for Media Files

EduMore360 uses Wasabi Cloud Storage for storing media files. This document explains how to work with Wasabi storage in the application.

## Configuration

The Wasabi storage is configured in `settings.py` with the following settings:

```python
# Wasabi Cloud Storage Settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Wasabi credentials from environment variables
AWS_ACCESS_KEY_ID = env('WASABI_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = env('WASABI_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = env('WASABI_BUCKET_NAME')
AWS_S3_REGION_NAME = env('WASABI_REGION')

# Wasabi specific settings
AWS_S3_ENDPOINT_URL = f'https://s3.{AWS_S3_REGION_NAME}.wasabisys.com'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = False
AWS_QUERYSTRING_EXPIRE = 3600

# Media files URL
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.wasabisys.com/'
```

## Environment Variables

The Wasabi credentials are stored in the `.env` file:

```
# Wasabi Cloud Storage
WASABI_ACCESS_KEY=your-access-key
WASABI_SECRET_KEY=your-secret-key
WASABI_BUCKET_NAME=your-bucket-name
WASABI_REGION=us-east-1
```

## Public Access

We're using public-read ACL for files, which means:

1. All files are publicly accessible via their URLs
2. No authentication or signed URLs are required
3. URLs are permanent and don't expire

## Using Media Files in Templates

To use media files in templates, use the `media_url` template tag:

```html
{% load media_tags %}
<img src="{% media_url object.image.name %}">
```

## Uploading Files

When uploading files, use Django's standard file handling:

```python
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Upload a file
path = default_storage.save('path/to/file.jpg', ContentFile(file_content))

# Get the URL
url = default_storage.url(path)
```

## Migrating Existing Media Files

To migrate existing media files to Wasabi, use the `migrate_to_wasabi.py` script:

```bash
python scripts/migrate_to_wasabi.py
```

## Testing Wasabi Storage

To test Wasabi storage, use the `test_wasabi.py` script:

```bash
python scripts/test_wasabi.py
```

## Troubleshooting

If you encounter issues with Wasabi storage:

1. Check that your Wasabi credentials are correct in the `.env` file
2. Verify that the bucket exists and is accessible
3. Check that the file permissions are set correctly
4. Ensure that the URLs are being generated correctly with the `media_url` template tag

## Important Notes

1. Wasabi free tier includes 1TB of storage
2. No egress fees (unlike most cloud providers)
3. S3-compatible API (works with django-storages)
4. Simple pricing model
