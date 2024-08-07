from django import template


register = template.Library()


@register.filter
def nan_to_empty(value):
    if value == 'nan':
        return ''
    return value
