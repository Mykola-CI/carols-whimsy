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
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity

        self.save_cart()

    def update(self, product, quantity):
        """
        Update the product quantity in the cart.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id] = quantity
            self.save_cart()

    def save_cart(self):
        """ Save the cart """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    @property
    def is_empty(self):
        """ Check if the cart is empty """

        return not bool(self.cart)  # Return True if the cart is empty

    @property
    def get_products(self):
        """ Get the products in the cart """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        return products

    @property
    def get_cart(self):
        """ Get the cart """
        return self.cart

    @property
    def get_totals(self):
        """ Get the cart totals """

        total = 0
        for product_id, quantity in self.cart.items():
            product_id = int(product_id)
            product = Product.objects.get(id=product_id)
            total += product.price * quantity

        return total

    def get_subtotal(self, product_id):
        """ Get the cart totals """

        product_id = str(product_id)
        subtotal = 0
        product = Product.objects.get(id=product_id)
        subtotal += product.price * self.cart[product_id]

        return subtotal
