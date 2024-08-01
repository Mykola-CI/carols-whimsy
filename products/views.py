from django.shortcuts import render

from .models import Product, Brand, Category, Theme, Season


def catalog(request):
    """ A view to return the catalog page """

    products = Product.objects.all()

    return render(request, 'products/catalog.html', {'products': products})
