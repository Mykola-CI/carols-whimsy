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
from user_profile.models import UserProfile, ShippingAddress
from .utils import get_billing_name


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        cart = Cart(request)
        cart_totals = cart.get_totals

        # Get the cart content from the session
        current_cart = request.session.get(settings.CART_SESSION_ID, {})
        promo_discount = int(request.session.get('promo_discount', 0))
        saving = round((cart_totals * promo_discount / 100), 2)

        ship_cost = cart.get_ship_cost

        # Update the payment intent with the shipping details and cart_content
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(current_cart),
            'shipping_cost': str(ship_cost),
            'saving': str(saving),
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
            # Save the form data to the User's shipping addresses
            if request.user.is_authenticated:
                if order_form.cleaned_data.get('save_address'):
                    ShippingAddress.objects.create(
                        user_profile=request.user.userprofile,
                        delivery_first_name=order_form.cleaned_data[
                            'first_name'],
                        delivery_last_name=order_form.cleaned_data[
                            'last_name'],
                        delivery_phone_number=order_form.cleaned_data[
                            'phone_number'],
                        delivery_email=order_form.cleaned_data['email'],
                        shipping_street_address=order_form.cleaned_data[
                            'street_address'],
                        shipping_town_city=order_form.cleaned_data[
                            'town_city'],
                        shipping_county=order_form.cleaned_data[
                            'county'],
                        shipping_postcode=order_form.cleaned_data[
                            'postcode'],
                        shipping_country=order_form.cleaned_data['country'],
                    )
            # Save the form data in the session for saving order later
            request.session['shipping_details'] = order_form.cleaned_data
            return redirect('checkout_payment')
        else:
            messages.error(
                request,
                'There was an error with your form. '
                'Please double check your information.'
                ' Or check your Internet connection.'
            )

    # Prefill the form with any info the user maintains in their profile
    if request.user.is_authenticated:
        # Check if the profile data has been used and set the flag
        if not request.session.get('profile_data_used', False):
            default_address = ShippingAddress.objects.filter(
                user_profile__user=request.user, shipping_is_default=True
            ).first()

            if default_address:
                order_form = OrderForm(initial={
                    'first_name': default_address.delivery_first_name,
                    'last_name': default_address.delivery_last_name,
                    'email': default_address.delivery_email,
                    'phone_number': default_address.delivery_phone_number,
                    # Convert country field to the string as not serializable
                    'country': str(default_address.shipping_country),
                    'postcode': default_address.shipping_postcode,
                    'town_city': default_address.shipping_town_city,
                    'street_address': default_address.shipping_street_address,
                    'county': default_address.shipping_county,
                })
                # Store the initial profile data in the session
                request.session['shipping_details'] = order_form.initial

                # Set the session flag to true as a signal that the db data has
                # been used to prefill the form
                request.session['profile_data_used'] = True

            else:
                # Render an empty form if no default address is found
                order_form = OrderForm()

        else:
            # Use new data from session if profile data has already been used
            order_form = OrderForm(
                initial=request.session.get('shipping_details', {}))
    else:
        # For anonymous users, use session data
        order_form = OrderForm(
            initial=request.session.get('shipping_details', {}))

    cart = Cart(request)
    warnings = cart._check_and_update_stock()  # Get warnings from stock check

    for warning in warnings:
        messages.warning(request, warning)  # Add each warning as a message

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

    user = request.user

    # Define the billing details for both authenticated and anonymous users
    if user.is_authenticated:
        # Get the billing name for the user using the utility function
        billing_name = get_billing_name(user)
        billing_details = {
            'billing_name': billing_name,
            'billing_email': user.email,
            'billing_phone_number': user.userprofile.profile_phone_number,
        }

    else:   # For anonymous users
        billing_name = (
            f"{shipping_details['first_name']} "
            f"{shipping_details['last_name']}"
        )
        billing_details = {
            'billing_name': billing_name,
            'billing_email': shipping_details['email'],
            'billing_phone_number': shipping_details['phone_number'],
        }

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        pid = request.POST.get('client_secret').split('_secret')[0]

        return redirect(reverse('order_pending', args=[pid]))

    else:
        cart = Cart(request)

        if cart.is_empty:
            messages.error(
                request, "There's nothing in your cart at the moment")
            return redirect('catalog')

        cart_totals = cart.get_totals
        promo_discount = int(request.session.get('promo_discount', 0))
        saving = round((cart_totals * promo_discount / 100), 2)

        ship_cost = cart.get_ship_cost
        grand_total = cart_totals - saving + ship_cost
        stripe_total = round(grand_total * 100)

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        client_secret = intent.client_secret

    context = {
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
        'shipping_details': shipping_details,
        'billing_details': billing_details,
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

    from_profile = request.GET.get('from_profile', 'false') == 'true'

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
        'from_profile': from_profile,
    }
    cart = Cart(request)
    cart.clear()
    request.session['promo_discount'] = 0

    return render(request, template, context)
