from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from products.models import Product, Brand, Category, Theme, Season
from checkout.models import Order, OrderLineItem
from .forms import ProductForm, OrderStatusForm


@login_required
def view_vendor_dashboard(request):
    """ A view to return the vendor dashboard """

    if not request.user.is_staff:
        messages.error(request, 'Sorry, only store stuff is granted access.')
        return redirect(reverse('home'))

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

    orders_pending_count = orders_pending.count()
    orders_processing_count = orders_processing.count()
    orders_shipped_count = orders_shipped.count()
    orders_not_shipped_count = orders_not_shipped.count()
    orders_not_delivered_count = orders_not_delivered.count()

    all_products_count = products.count()

    products_by_brand = {
        brand.id: products.filter(brand=brand).count()
        for brand in brands
    }

    products_by_category = {
        category.id: products.filter(category=category).count()
        for category in categories
    }

    products_by_theme = {
        theme.id: products.filter(theme=theme).count()
        for theme in themes
    }

    products_by_season = {
        season.id: products.filter(season=season).count()
        for season in seasons
    }

    context = {
            'products': products,
            'all_products_count': all_products_count,
            'products_by_brand': products_by_brand,
            'products_by_category': products_by_category,
            'products_by_theme': products_by_theme,
            'products_by_season': products_by_season,
            'orders_pending': orders_pending_count,
            'orders_processing': orders_processing_count,
            'orders_shipped': orders_shipped_count,
            'orders_not_shipped': orders_not_shipped_count,
            'orders_not_delivered': orders_not_delivered_count,
        }

    return render(request, 'vendor/vendor_dashboard.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """

    if not request.user.is_staff:
        messages.error(request, 'Sorry, only store stuff is granted access.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. '
                                    'Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'vendor/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    if not request.user.is_staff:
        messages.error(request, 'Sorry, only store stuff is granted access.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. '
                                    'Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'vendor/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """

    if not request.user.is_staff:
        messages.error(request, 'Sorry, only store stuff is granted access.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('view_dashboard'))


@login_required
def view_orders(request):
    """ A view to return the orders in progress """

    if not request.user.is_staff:
        messages.error(request, 'Sorry, only store stuff is granted access.')
        return redirect(reverse('home'))

    orders = Order.objects.all()

    orders_except_delivered = orders.filter(
        Q(status='Pending') | Q(status='Processing') | Q(status='Shipped')
    ).order_by('date')  # Order by date from older to newer

    order_count = orders_except_delivered.count()

    orders_with_items = []
    for order in orders_except_delivered:
        line_items = OrderLineItem.objects.filter(order=order)
        orders_with_items.append({
            'order': order,
            'line_items': line_items
        })

    form = OrderStatusForm()

    context = {
        'orders_with_items': orders_with_items,
        'order_count': order_count,
        'form': form,
    }

    return render(request, 'vendor/vendor_orders.html', context)


@login_required
def update_order_status(request, order_id):
    """ Update the status of an order"""

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)

        if form.is_valid() and form.cleaned_data['status'] != '':
            form.save()
            messages.success(request, 'Order status updated successfully!')
            return redirect('view_orders')
        else:
            messages.error(request, 'Please select a valid order status.')
            return redirect('view_orders')
