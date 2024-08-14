import os
from django import template
from django.conf import settings


register = template.Library()


@register.filter
def nan_to_empty(value):
    if value == 'nan':
        return ''
    return value


@register.filter
def get_quantity(cart_items, product_id):
    # Convert product_id to string to match the keys in cart_items
    product_id_str = str(product_id)
    # Retrieve the quantity from cart_items
    return cart_items.get(product_id_str, 0)


@register.filter(name='image_exists')
def image_exists(image_field):
    if not image_field or not hasattr(image_field, 'name') or not image_field.name:
        return False
    full_path = os.path.join(settings.MEDIA_ROOT, image_field.name)
    return os.path.isfile(full_path)
