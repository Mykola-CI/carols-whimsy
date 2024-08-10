from .cart import Cart


def cart(request):
    """
    Cart context processor so our Cart object can be available
    in all templates across the site
    """

    cart = Cart(request)
    cart_products = cart.get_products
    items_quantities = cart.get_cart
    cart_status = cart.is_empty

    context = {
        'cart_status': cart_status,
        'cart_products': cart_products,
        'items_quantities': items_quantities
    }

    return context
