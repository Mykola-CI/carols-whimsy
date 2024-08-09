from django.conf import settings

from products.models import Product


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

    def add(self, product_id, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product_id)  # Ensure the product_id is a string
        print(product_id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity}

        self.save()

    def save(self):
        self.session.modified = True
