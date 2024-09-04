from .cart import Cart
from vendor.models import CommercialConstant


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
    number_of_items = sum(items_quantities.values())

    cart_subtotals = {}
    for product in cart_products:
        cart_subtotals[str(product.id)] = cart.get_subtotal(
            product_id=product.id)

    promo_discount = int(request.session.get('promo_discount', 0))
    saving = round((cart_totals * promo_discount / 100), 2)
    shipping = cart.get_ship_cost
    threshold = CommercialConstant.objects.get(
        name='free_delivery_threshold').get_value()

    grand_total = round((cart_totals + shipping - saving), 2)

    context = {
        'cart_status': cart_status,
        'cart_products': cart_products,
        'items_quantities': items_quantities,
        'cart_totals': cart_totals,
        'cart_subtotals': cart_subtotals,
        'saving': saving,
        'ship_cost': shipping,
        'grand_total': grand_total,
        'number_of_items': number_of_items,
        'delivery_threshold': threshold,
    }

    return context
