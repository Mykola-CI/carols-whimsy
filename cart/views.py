from django.shortcuts import render
from django.http import JsonResponse

from .cart import Cart


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        # Add the product to the cart
        cart = Cart(request)
        cart.add(product_id, quantity)

        return JsonResponse({'message': 'Product added to cart successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_update(request):
    pass


def cart_remove(request):
    pass
