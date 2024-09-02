from django import template


register = template.Library()


# The filter that converts a string 'nan' to an empty string
# This is used to avoid errors when displaying NaN values in the template,
# occurred during excel file import
@register.filter
def nan_to_empty(value):
    if value == 'nan':
        return ''
    return value


# This filter gets the value of a key from a dictionary. Used in the vendor app
@register.filter
def dict_get(dictionary, key):
    if dictionary is None:
        return 0
    try:
        return dictionary[key]
    except KeyError:
        return 0
