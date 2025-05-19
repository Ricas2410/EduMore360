"""
Template tags for handling media files.
"""

from django import template
from django.core.files.storage import default_storage

register = template.Library()

@register.simple_tag
def media_url(file_path):
    """
    Generate a URL for a media file.

    For public storage (like Wasabi with public-read ACL), this returns a direct URL.
    For private storage, this returns a signed URL with an expiration time.

    Usage:
    {% load media_tags %}
    <img src="{% media_url 'path/to/image.jpg' %}">
    """
    if not file_path:
        return ''

    try:
        # Ensure the file path uses forward slashes
        file_path = file_path.replace('\\', '/')

        # Use Django's default_storage.url method to generate a signed URL
        url = default_storage.url(file_path)
        return url
    except Exception as e:
        # Log the error and return an empty string
        print(f"Error generating URL for {file_path}: {e}")
        return ''
