from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .cart import Cart
from products.models import Product, Brand, Category, Theme, Season


def cart_summary(request):
    """
    Summary view of the cart
    Keyword arguments: request -- the full HTTP request object
    Return: render the cart summary template
    """

    brands = Brand.objects.all()
    categories = Category.objects.all()
    themes = Theme.objects.all()
    seasons = Season.objects.all()
    products = Product.objects.all()

    context = {
        'brands': brands,
        'categories': categories,
        'themes': themes,
        'seasons': seasons,
        'products': products,
    }

    return render(request, 'cart/cart_summary.html', context)


@require_POST
def add_to_cart(request):
    """
    Add a product to the cart
    """

    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity', 1)

    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1  # Ensure minimum quantity is 1
    except (ValueError, TypeError):
        quantity = 1  # Default to 1 if invalid

    # Just checking if the product exists, if not, return a 404
    product = get_object_or_404(Product, pk=product_id)

    try:
        cart = Cart(request)
        cart.add(product=product, quantity=quantity)
        messages.success(
            request, f'Added ({quantity}) item(s) of '
                     f'"{product.name}" to your cart. '
                     f'Click on the Cart button to view your cart.')

    except Exception as e:
        messages.error(
            request, "There was an error adding the product to your cart.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error'}, status=500)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = int(request.POST.get('quantity'))

        # Check if the product exists
        product = get_object_or_404(Product, pk=product_id)

        cart = Cart(request)
        # Retrieve the old quantity for the product before the update
        old_quantity = cart.cart.get(str(product_id), 0)
        print(f'Old Quantity: {old_quantity}')
        # Update the product quantity in the cart
        cart.update(product=product, quantity=new_quantity)

        messages.success(
            request, f'Updated quantity of "{product.name}" from '
                     f'({old_quantity}) to ({new_quantity}). '
                     f'Click on the Cart button to view your cart.')

        return JsonResponse(
            {'status': 'success'}, status=200)


def remove_item(request, product_id):

    cart = Cart(request)
    product_item = get_object_or_404(Product, pk=product_id)
    name = product_item.name
    cart.delete_item(product_id)

    messages.info(
            request, f'Removed "{name}" from cart.')

    return redirect('cart_summary')


def clear_cart(request):

    cart = Cart(request)
    cart.clear()

    messages.info(request, 'Cart has been cleared.')

    return redirect('cart_summary')
