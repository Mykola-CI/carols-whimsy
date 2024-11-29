from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Product, Brand, Category, Theme, Season
from .convert_price_utility import convert_price


def catalog(request):
    """ A view to return the catalog page """

    # Get the selected currency from the session, default to GBP if not set
    target_currency = request.session.get("currency", "GBP")

    # Optimize queries with select_related and prefetch_related
    products = Product.objects.select_related(
        'brand', 'category', 'theme', 'season')

    # Convert each product's price to the target currency
    for product in products:
        # Assuming `price` is a MoneyField, it already contains currency information
        converted_price = convert_price(product.price_money, target_currency)
        product.converted_price = converted_price
        product.discounted_price_converted = (
            product.get_discounted_price_converted(target_currency))

    search = None
    sortkey = None

    if request.GET:
        if 'brand_query' in request.GET:
            brand = request.GET['brand_query']
            products = products.filter(brand__name=brand)
        if 'category_query' in request.GET:
            category = request.GET['category_query']
            products = products.filter(category__name=category)
        if 'theme_query' in request.GET:
            theme = request.GET['theme_query']
            products = products.filter(theme__name=theme)
        if 'season_query' in request.GET:
            season = request.GET['season_query']
            products = products.filter(season__name=season)
        if 'deals_query' in request.GET:
            products = products.filter(discount__gt=0)
        if 'preorder_status' in request.GET and request.GET['preorder_status']:
            try:
                preorder_status = int(request.GET['preorder_status'])
                products = products.filter(preorder_status=preorder_status)
            except ValueError:
                # Invalid preorder_status value - skip this filter
                pass

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
                Q(size__icontains=search)
            )
            products = products.filter(queries)

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey == 'price_asc':
                products = products.order_by('price')
            if sortkey == 'price_desc':
                products = products.order_by('-price')

    products_count = products.count()

    context = {
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'themes': Theme.objects.all(),
        'seasons': Season.objects.all(),
        'products': products,
        'products_count': products_count,
        'sortkey': sortkey,
        'preorder_status_choices': Product.PREORDER_STATUS_CHOICES,
    }

    return render(request, 'products/catalog.html', context)


def product_detail(request, product_id):
    """ A view to return the product detail page """

    brands = Brand.objects.all()
    categories = Category.objects.all()
    themes = Theme.objects.all()
    seasons = Season.objects.all()

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'brands': brands,
        'categories': categories,
        'themes': themes,
        'seasons': seasons,
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def set_currency(request):
    if request.method == "POST":
        selected_currency = request.POST.get("currency", "GBP")
        request.session["currency"] = selected_currency
    return redirect(request.META.get("HTTP_REFERER", "/"))
