from django import template


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
