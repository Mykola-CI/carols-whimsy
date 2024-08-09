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

    def add(self, product, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)  # Ensure the product_id is a string

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'name': product.name,
                'quantity': quantity,
                'price': str(product.price),
            }

        self.save_cart()

    def save_cart(self):
        """ Save the cart """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    @property
    def is_empty(self):
        """ Check if the cart is empty """
        print(not bool(self.cart))
        return not bool(self.cart)  # Return True if the cart is empty

    @property
    def items(self):
        return [
            (item.get('name', 'Empty'),
             item.get('quantity', 0),
             item.get('price', '0'))
            for item in self.cart.values()
        ]
