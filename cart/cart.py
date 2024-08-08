from django.conf import settings


class Cart():
    """ Cart functionality setting class """

    def __init__(self, request):
        """ Initialize the cart """
        self.session = request.session

        # Get the cart from the session if it exists
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        # Ensure the cart is always available during customer interactions
        self.cart = cart
