import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='clean_html')
def clean_html(value):
    """
    Clean HTML content by removing data attributes and fixing formatting issues.
    """
    if value is None:
        return ''
    
    # Remove data attributes
    value = re.sub(r'\s*data-[a-zA-Z0-9_\-]+="[^"]*"', '', value)
    
    # Remove empty class attributes
    value = re.sub(r'\s*class=""', '', value)
    
    # Fix multiple consecutive line breaks
    value = re.sub(r'(\s*<br\s*/?>){2,}', '<br>', value)
    
    # Fix spacing around headings
    value = re.sub(r'(<h[1-6][^>]*>)\s+', r'\1', value)
    value = re.sub(r'\s+(</h[1-6]>)', r'\1', value)
    
    # Fix spacing around paragraphs
    value = re.sub(r'(<p[^>]*>)\s+', r'\1', value)
    value = re.sub(r'\s+(</p>)', r'\1', value)
    
    return mark_safe(value)
