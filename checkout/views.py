from django.shortcuts import render
from products.models import Product, Brand, Category, Theme, Season


def checkout_shipping(request):
    """ A view to return the index page """

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

    return render(request, 'checkout/checkout-shipping.html', context)
