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
    cart_totals = cart.get_totals

    cart_subtotals = {}
    for product in cart_products:
        cart_subtotals[str(product.id)] = (
            product.price * items_quantities[str(product.id)]
        )

    saving = 0
    ship_cost = 0
    grand_total = cart_totals + ship_cost - saving

    context = {
        'cart_status': cart_status,
        'cart_products': cart_products,
        'items_quantities': items_quantities,
        'cart_totals': cart_totals,
        'cart_subtotals': cart_subtotals,
        'saving': saving,
        'ship_cost': ship_cost,
        'grand_total': grand_total,
    }

    return context
