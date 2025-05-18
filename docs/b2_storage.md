# Using Backblaze B2 for Media Storage

EduMore360 uses Backblaze B2 Cloud Storage for storing media files. This document explains how to work with B2 storage in the application.

## Configuration

The B2 storage is configured in `settings.py` with the following settings:

```python
# B2 credentials
AWS_ACCESS_KEY_ID = env('B2_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('B2_APPLICATION_KEY')
AWS_STORAGE_BUCKET_NAME = env('B2_BUCKET_NAME')

# B2 specific settings
AWS_S3_ENDPOINT_URL = 'https://s3.us-east-005.backblazeb2.com'
AWS_S3_REGION_NAME = 'us-east-005'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'private'  # Use private ACL for files
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = True  # Enable query string authentication for URLs
AWS_QUERYSTRING_EXPIRE = 3600  # URLs expire after 1 hour (3600 seconds)
```

## Private Buckets and Signed URLs

We're using private buckets for security reasons. This means:

1. All URLs are signed and expire after 1 hour by default
2. For user-uploaded content, the URLs will need to be refreshed if accessed after expiration
3. For static content like images on your site, consider using a CDN like Cloudflare

## Using Media Files in Templates

To use media files in templates, use the `media_url` template tag:

```html
{% load media_tags %}
<img src="{% media_url object.image.name %}">
```

This will generate a signed URL for the media file that will work for 1 hour.

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

To migrate existing media files to B2, use the `migrate_media_to_b2.py` script:

```bash
python scripts/migrate_media_to_b2.py
```

## Testing B2 Storage

To test B2 storage, use the `test_media_upload.py` script:

```bash
python scripts/test_media_upload.py
```

## Troubleshooting

If you encounter issues with B2 storage:

1. Check that your B2 credentials are correct in the `.env` file
2. Verify that the bucket exists and is accessible
3. Check that the file permissions are set correctly
4. Ensure that the URLs are being generated correctly with the `media_url` template tag

## Important Notes

1. B2 free tier includes 10GB of storage and 1GB of daily downloads
2. Private buckets require generating signed URLs for access
3. Signed URLs expire after 1 hour by default (configurable)
4. For production, consider adding a CDN like Cloudflare in front of B2
