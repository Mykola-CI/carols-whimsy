from django.shortcuts import (render, redirect, reverse,
                              HttpResponse, get_object_or_404)
from django.http import JsonResponse
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
from user_profile.models import UserProfile


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

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
            messages.error(
                request,
                'There was an error with your form. '
                'Please double check your information.'
            )

    # Prefill the form with any info the user maintains in their profile
    if request.user.is_authenticated:
        # Check if the profile data has been used and set the flag
        if not request.session.get('profile_data_used', False):
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'first_name': profile.user.first_name,
                    'last_name': profile.user.last_name,
                    'email': profile.user.email,
                    'phone_number': profile.profile_phone_number,
                    # Convert country field to the string as not serializable
                    'country': str(profile.profile_country),
                    'postcode': profile.profile_postcode,
                    'town_city': profile.profile_town_city,
                    'street_address': profile.profile_street_address,
                    'county': profile.profile_county,
                })

                # Store the initial profile data in the session
                request.session['shipping_details'] = order_form.initial

                # Set the session flag to true as a signal that the db data has
                # been used to prefill the form
                request.session['profile_data_used'] = True
            except UserProfile.DoesNotExist:
                order_form = OrderForm()

        else:
            # Use new data from session if profile data has already been used
            order_form = OrderForm(
                initial=request.session.get('shipping_details', {}))
    else:
        # For anonymous users, use session data
        order_form = OrderForm(
            initial=request.session.get('shipping_details', {}))

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
        pid = request.POST.get('client_secret').split('_secret')[0]
        print(pid)
        return redirect(reverse('order_pending', args=[pid]))

    else:
        cart = Cart(request)
        if cart.is_empty:
            messages.error(
                request, "There's nothing in your cart at the moment")
            return redirect('catalog')

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


def order_pending(request, pid):
    # Render the order_pending template with the PID as context
    return render(request, 'checkout/order-pending.html', {'pid': pid})


def check_order_status(request, pid):
    order_exists = Order.objects.filter(stripe_pid=pid).exists()
    if order_exists:
        order = Order.objects.get(stripe_pid=pid)
        return JsonResponse(
            {'order_exists': True, 'order_number': order.order_number})
    return JsonResponse({'order_exists': False})


def order_confirmation(request, order_number):
    """
    A view to return the order confirmation page
    for the payment method type: card
    """

    order = get_object_or_404(Order, order_number=order_number)
    order_line_items = OrderLineItem.objects.filter(order=order)
    country_code = order.country
    # Get the full country name
    country_name = countries.name(country_code)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attaching the user's profile to the order
        order.user_profile = profile
        order.save()

    template = 'checkout/order-confirmation.html'

    context = {
        'order': order,
        'order_line_items': order_line_items,
        'country_name': country_name,
    }
    cart = Cart(request)
    cart.clear()

    return render(request, template, context)


# def checkout_success(request, pid):
#     """ A view to return the order confirmation page """

#     order = get_object_or_404(Order, stripe_pid=pid)
#     order_line_items = OrderLineItem.objects.filter(order=order)
#     country_code = order.country
#     # Get the full country name
#     country_name = countries.name(country_code)

#     if request.user.is_authenticated:
#         profile = UserProfile.objects.get(user=request.user)
#         # Attaching the user's profile to the order
#         order.user_profile = profile
#         order.save()

#     template = 'checkout/order-confirmation.html'

#     context = {
#         'order': order,
#         'order_line_items': order_line_items,
#         'country_name': country_name,
#     }
#     cart = Cart(request)
#     cart.clear()

#     return render(request, template, context)


# def order_interruption(request):
#     """ A view to return the index page """

#     template = 'checkout/order-interruption.html'

#     context = {}

#     return render(request, template, context)
