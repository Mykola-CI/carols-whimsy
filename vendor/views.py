from django.shortcuts import render
from django.db.models import Q

from products.models import Product, Brand, Category, Theme, Season
from checkout.models import Order


def view_vendor_dashboard(request):
    """ A view to return the vendor dashboard """

    brands = Brand.objects.all()
    categories = Category.objects.all()
    themes = Theme.objects.all()
    seasons = Season.objects.all()
    products = Product.objects.all()

    orders = Order.objects.all()

    orders_pending = orders.filter(status='Pending')
    orders_processing = orders.filter(status='Processing')
    orders_shipped = orders.filter(status='Shipped')
    orders_not_shipped = orders.filter(
        Q(status='Pending') | Q(status='Processing')
    )
    orders_not_delivered = orders.filter(
        Q(status='Pending') | Q(status='Processing') | Q(status='Shipped')
    )

    all_products_count = products.count()

    products_by_brand = {
        brand.name: products.filter(brand=brand).count()
        for brand in brands
    }

    products_by_category = {
        category.name: products.filter(category=category).count()
        for category in categories
    }

    products_by_theme = {
        theme.name: products.filter(theme=theme).count()
        for theme in themes
    }

    products_by_season = {
        season.name: products.filter(season=season).count()
        for season in seasons
    }

    context = {
            'products': products,
            'all_products_count': all_products_count,
            'products_by_brand': products_by_brand,
            'products_by_category': products_by_category,
            'products_by_theme': products_by_theme,
            'products_by_season': products_by_season,
            'orders_pending': orders_pending,
            'orders_processing': orders_processing,
            'orders_shipped': orders_shipped,
            'orders_not_shipped': orders_not_shipped,
            'orders_not_delivered': orders_not_delivered,
        }

    return render(request, 'vendor/vendor_dashboard.html', context)
