from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from cart.cart import Cart
from .forms import OrderForm
from django_countries import countries
from django.conf import settings
import stripe


def checkout_shipping(request):
    """ A view to return the index page """

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            request.session['shipping_details'] = order_form.cleaned_data
            return redirect(reverse('checkout_payment'))
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

    cart = Cart(request)
    if cart.is_empty:
        messages.error(
            request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    total = cart.get_totals
    stripe_total = round(total * 100)

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    print(intent)

    client_secret = intent.client_secret

    context = {
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
        'shipping_details': shipping_details,
        'country_name': country_name,
    }

    template = 'checkout/checkout-payment.html'

    return render(request, template, context)
