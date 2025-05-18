"""
Template tags for handling media files.
"""

from django import template
from django.core.files.storage import default_storage

register = template.Library()

@register.simple_tag
def media_url(file_path):
    """
    Generate a signed URL for a media file.
    
    Usage:
    {% load media_tags %}
    <img src="{% media_url 'path/to/image.jpg' %}">
    """
    if not file_path:
        return ''
    
    try:
        # Generate a signed URL for the file
        url = default_storage.url(file_path)
        return url
    except Exception as e:
        # Log the error and return an empty string
        print(f"Error generating URL for {file_path}: {e}")
        return ''
