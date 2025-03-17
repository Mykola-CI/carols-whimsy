from django.conf import settings
from django.contrib import messages

from products.models import Product
from vendor.models import CommercialConstant


class Cart:
    """Cart functionality setting class"""

    def __init__(self, request):
        """Initialize the cart"""
        self.session = request.session

        # Get the cart from the session if it exists
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        # Ensure the cart is always available during customer interactions
        self.cart = cart

        # Check stock levels and update quantities
        # self.warnings = self._check_and_update_stock()

    def _check_and_update_stock(self):
        """Check stock levels and update cart quantities"""

        updated_cart = self.cart.copy()
        warnings = []  # Collect warning messages

        for product_id, quantity in self.cart.items():
            try:
                # Fetch product stock level from the database
                product = Product.objects.get(id=product_id)
                if quantity > product.stock and product.stock > 0:
                    # Update quantity to match stock level
                    updated_cart[product_id] = product.stock

                    warnings.append(
                        f"We had to decrease the quantity of \n"
                        f"'{product.name}' to {product.stock} item(s) in "
                        f"line with the available stock. \n"
                        f"Somebody must have been ahead of you. Sorry!"
                    )

                elif product.stock == 0:
                    warnings.append(
                        f"Unfortunately we had to remove the \n"
                        f"'{product.name}' from your cart as it is no longer "
                        f"available. "
                        f"Somebody must have been ahead of you. Sorry!"
                    )
                    # Remove product from cart if stock is depleted
                    updated_cart.pop(product_id)

            except Product.DoesNotExist:
                # If product is not found, remove it from the cart
                updated_cart.pop(product_id)

        # Save updated cart back to session
        self.cart = updated_cart
        self.session[settings.CART_SESSION_ID] = updated_cart
        self.session.modified = True

        return warnings  # Always return a list (even if empty)

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

    def delete_item(self, product_id):
        """Remove an item from the cart"""
        product_id = str(product_id)

        print(f"Print out from the Cart: {product_id}")

        if product_id in self.cart:
            self.cart.pop(product_id)
            self.save_cart()

    def clear(self):
        """Clear the cart"""
        self.cart = {}
        self.save_cart()

    def save_cart(self):
        """Save the cart"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    @property
    def is_empty(self):
        """Check if the cart is empty"""

        return not bool(self.cart)  # Return True if the cart is empty

    @property
    def get_products(self):
        """Get the products in the cart"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        return products

    @property
    def get_cart(self):
        """Get the cart"""
        return self.cart

    @property
    def get_totals(self):
        """Get the cart totals"""

        total = 0
        for product_id, quantity in self.cart.items():
            product_id = int(product_id)
            product = Product.objects.get(id=product_id)
            total += product.price * quantity

        return total

    def get_subtotal(self, product_id):
        """Get the cart totals"""

        product_id = str(product_id)
        subtotal = 0
        product = Product.objects.get(id=product_id)
        subtotal += product.price * self.cart[product_id]

        return subtotal

    @property
    def get_ship_cost(self):
        """Get the shipping cost"""
        delivery_threshold = CommercialConstant.objects.get(
            name="free_delivery_threshold"
        )
        delivery_percent = CommercialConstant.objects.get(name="delivery_percent")
        threshold = delivery_threshold.get_value()
        percent = delivery_percent.get_value()
        cart_totals = self.get_totals
        if cart_totals < threshold:
            ship_cost = round((cart_totals * percent / 100), 2)
        else:
            ship_cost = 0

        return ship_cost
