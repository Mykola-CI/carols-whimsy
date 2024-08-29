import stripe
from django.db import IntegrityError
from django.http import HttpResponse

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from cart.cart import Cart

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

        # Prepare the context for rendering the email subject and body
        context = {
            'order': order,
            'contact_email': settings.DEFAULT_FROM_EMAIL,
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

        if Order.objects.filter(stripe_pid=pid).exists():
            # Order already exists, do not create a new one
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Order already exists',
                status=200
            )
        else:
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

            try:
                order = Order(
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
                order.save()
                # Create order line items
                for item_id, quantity in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()

                # Send confirmation email
                # self._send_confirmation_email(order)

                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
                    status=200
                )

            except IntegrityError:
                # Handle the case where the order already exists due to a race condition
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: Order already exists',
                    status=200
                )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        intent = event.data.object

        return HttpResponse(
            # content=f'Webhook received: {event["type"]}',
            status=200)
