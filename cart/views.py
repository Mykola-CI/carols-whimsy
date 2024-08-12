from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

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

    # Add the product to the cart
    cart = Cart(request)
    cart.add(product=product, quantity=quantity)

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'message': 'Product added to cart successfully!'})
    else:
        # For regular form submissions, redirect back to the referring page
        # with filters intact
        referer = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referer)


def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = int(request.POST.get('quantity'))

        # Check if the product exists
        product = get_object_or_404(Product, pk=product_id)

        # Update the product quantity in the cart
        cart = Cart(request)
        cart.update(product=product, quantity=new_quantity)

        return JsonResponse(
            {'message': 'Cart updated successfully!'}
        )


def remove_item(request, product_id):

    cart = Cart(request)
    cart.delete_item(product_id)

    return redirect('cart_summary')


def clear_cart(request):

    cart = Cart(request)
    cart.clear()

    return redirect('cart_summary')
