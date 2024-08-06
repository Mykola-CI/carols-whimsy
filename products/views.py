from django.shortcuts import render

from .models import Product, Brand, Category, Theme, Season


def catalog(request):
    """ A view to return the catalog page """

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

    return render(request, 'products/catalog.html', context)
