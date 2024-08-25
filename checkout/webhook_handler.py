import stripe
from django.http import HttpResponse

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product

import json
import time
# import logging


# Set up logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.ERROR)  # You can configure this as needed


class WH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""

        customer_email = order.email

        # Access the UserProfile through the User model
        user_profile = order.user.userprofile

        # Retrieve the title from the UserProfile, or use an empty string
        # if it's 'None' or doesn't exist
        title = (
            user_profile.get_title_friendly_name() if user_profile and
            user_profile.title != 'None' else ''
        )
        # Prepare the context for rendering the email subject and body
        context = {
            'order': order,
            'contact_email': settings.DEFAULT_FROM_EMAIL,
            'title': title
        }

        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            context
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            context
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """

        intent = event.data.object
        pid = intent.id
        # Get the cart from the event's metadata
        cart = intent.metadata.cart

        # Get the Charge object for capturing of phone and email
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        # Get email from the charge object as it does not come in the intent
        email = stripe_charge.billing_details.email

        # Split full name onto first and last name
        full_name = intent.shipping.name
        first_name = full_name.split()[0]
        last_name = full_name.split()[-1] if len(full_name.split()) > 1 else ""

        phone = intent.shipping.phone
        street_address = intent.shipping.address.line1
        city = intent.shipping.address.city
        county = intent.shipping.address.state
        postal_code = intent.shipping.address.postal_code
        country = intent.shipping.address.country

        grand_total = round(stripe_charge.amount / 100, 2)  # updated

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    first_name__iexact=first_name,
                    last_name__iexact=last_name,
                    email__iexact=email,
                    phone_number__iexact=phone,
                    country__iexact=country,
                    postcode__iexact=postal_code,
                    town_city__iexact=city,
                    street_address__iexact=street_address,
                    county__iexact=county,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    f'SUCCESS: Verified order already in database'),
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone,
                    country=country,
                    postcode=postal_code,
                    town_city=city,
                    street_address=street_address,
                    county=county,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for item_id, quantity in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()

            except Exception as e:
                if 'order' in locals() and order:
                    order.delete()

                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500
                )

        self._send_confirmation_email(order)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | '
                    f'SUCCESS: Created order in webhook', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        intent = event.data.object

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
