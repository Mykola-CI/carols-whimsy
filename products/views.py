from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q

from .models import Product, Brand, Category, Theme, Season


def catalog(request):
    """ A view to return the catalog page """

    brands = Brand.objects.all()
    categories = Category.objects.all()
    themes = Theme.objects.all()
    seasons = Season.objects.all()
    products = Product.objects.all()

    search = None
    brand = None

    if request.GET:
        if 'brand_query' in request.GET:
            brand = request.GET['brand_query']
            products = products.filter(brand__name=brand)

        if 'search' in request.GET:
            search = request.GET['search']
            if not search:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('catalog'))

            queries = (
                Q(name__icontains=search) |
                Q(promo_text__icontains=search) |
                Q(color__icontains=search) |
                Q(material__icontains=search) |
                Q(other_details__icontains=search)
            )
            products = products.filter(queries)

    products_count = products.count()
    print(products_count)

    context = {
        'brands': brands,
        'categories': categories,
        'themes': themes,
        'seasons': seasons,
        'products': products,
        'search_status': search,
        'products_count': products_count,
    }

    return render(request, 'products/catalog.html', context)
