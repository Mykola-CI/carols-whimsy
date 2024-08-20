from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from cart.cart import Cart
from .forms import OrderForm
from django_countries import countries
from django.conf import settings
import stripe
import json

from .models import Order, OrderLineItem
from products.models import Product


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the shipping details from the session
        # shipping_details = request.session.get('shipping_details', {})

        # Get the cart content from the session
        current_cart = request.session.get(settings.CART_SESSION_ID, {})

        # Update the payment intent with the shipping details and cart_content
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(current_cart),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout_shipping(request):
    """ A view to return the index page """

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            request.session['shipping_details'] = order_form.cleaned_data
            return redirect('checkout_payment')
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

    # Populate form with existing session data if available
    order_form = OrderForm(initial=request.session.get('shipping_details'))

    template = 'checkout/checkout-shipping.html'

    context = {
        'order_form': order_form,
    }

    return render(request, template, context)


def checkout_payment(request):
    """ A view to return the index page """

    shipping_details = request.session.get('shipping_details', {})

    country_code = shipping_details.get('country')
    # Get the full country name
    country_name = countries.name(country_code)

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = Cart(request)
        if cart.is_empty:
            messages.error(
                request, "There's nothing in your cart at the moment")
            return redirect('products')

        order = Order(
            first_name=shipping_details.get('first_name'),
            last_name=shipping_details.get('last_name'),
            email=shipping_details.get('email'),
            phone_number=shipping_details.get('phone_number'),
            town_city=shipping_details.get('town_city'),
            county=shipping_details.get('county'),
            street_address=shipping_details.get('street_address'),
            postcode=shipping_details.get('postcode'),
            country=shipping_details.get('country'),
        )
        # Get PaymentIntentID from hidden input in the checkout-payment.html
        pid = request.POST.get('client_secret').split('_secret')[0]
        order.stripe_pid = pid
        # Serialize the cart content to store in the order
        order.original_cart = json.dumps(cart.cart)

        order.save()

        for item_id, quantity in cart.cart.items():
            try:
                product = Product.objects.get(id=item_id)
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
                order_line_item.save()
            except Product.DoesNotExist:
                messages.error(request, (
                    "One of the products in your cart wasn't found in "
                    "our database. "
                    "Please contact customer service for assistance!")
                )
                order.delete()
                return redirect('cart_summary')

        return redirect('order_confirmation')

    else:
        cart = Cart(request)
        if cart.is_empty:
            messages.error(
                request, "There's nothing in your cart at the moment")
            return redirect('products')

        total = cart.get_totals
        stripe_total = round(total * 100)

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        client_secret = intent.client_secret

    context = {
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
        'shipping_details': shipping_details,
        'country_name': country_name,
    }

    template = 'checkout/checkout-payment.html'

    return render(request, template, context)


def order_confirmation(request):
    """ A view to return the index page """

    shipping_details = request.session.get('shipping_details', {})

    if not shipping_details:
        return redirect('checkout_shipping')

    template = 'checkout/order-confirmation.html'

    context = {
        'shipping_details': shipping_details,
    }

    return render(request, template, context)
