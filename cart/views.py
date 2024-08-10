from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from products.models import Product


def cart_summary(request):
    """
    Summary view of the cart
    Keyword arguments: request -- the full HTTP request object
    Return: render the cart summary template
    """

    return render(request, 'cart/cart_summary.html')


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        # Just checking if the product exists, if not, return a 404
        product = get_object_or_404(Product, pk=product_id)

        # Add the product to the cart
        cart = Cart(request)
        cart.add(product=product, quantity=quantity)

        return JsonResponse(
            {'message': 'Product added to cart successfully!'}
        )


def cart_update(request):
    pass


def cart_remove(request):
    pass
