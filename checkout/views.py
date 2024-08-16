from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from cart.cart import Cart
from .forms import OrderForm
from django_countries import countries


def checkout_shipping(request):
    """ A view to return the index page """

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            request.session['shipping_details'] = order_form.cleaned_data
            return redirect(reverse('checkout_payment'))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

    order_form = OrderForm()
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

    context = {
        'shipping_details': shipping_details,
        'country_name': country_name,
    }

    template = 'checkout/checkout-payment.html'

    return render(request, template, context)
