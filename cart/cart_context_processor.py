from .cart import Cart


def cart(request):
    """
    Cart context processor so our Cart object can be available
    in all templates across the site
    """

    return {'cart': Cart(request)}
