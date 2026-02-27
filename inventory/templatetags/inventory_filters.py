from django import template

register = template.Library()


@register.filter(name='length_where')
def length_where(queryset, arg):
    """
    Returns the count of objects in a queryset where a field matches a value.
    Usage: {{ queryset|length_where:"status=OP" }}
    """
    if not queryset:
        return 0
    
    try:
        field, value = arg.split('=')
        return queryset.filter(**{field: value}).count()
    except (ValueError, AttributeError):
        return 0
