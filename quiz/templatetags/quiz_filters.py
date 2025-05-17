from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Custom template filter to get an item from a dictionary by key.
    Usage: {{ my_dict|get_item:key_variable }}
    """
    return dictionary.get(key)

@register.filter
def filter_by_id(queryset, id_value):
    """
    Custom template filter to get an item from a queryset by id.
    Usage: {{ queryset|filter_by_id:id_value }}
    Returns the first matching object or None.
    """
    try:
        # Convert id_value to int if it's a string
        if isinstance(id_value, str) and id_value.isdigit():
            id_value = int(id_value)

        # Try to find the object with the given id
        return queryset.filter(id=id_value).first()
    except (ValueError, AttributeError):
        return None
