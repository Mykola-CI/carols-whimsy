import stripe
from django.db import IntegrityError
from django.http import HttpResponse

from django.core.mail import send_mail
from django.template.loader import render_to_string
from decimal import Decimal
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product

import json


class WH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order, billing_details):
        """Send the user a confirmation email"""

        customer_email = billing_details['billing_email']

        # Prepare the context for rendering the email subject and body
        context = {
            'order': order,
            'contact_email': settings.DEFAULT_FROM_EMAIL,
            'billing_name': billing_details['billing_name'],
            'billing_email': billing_details['billing_email'],
            'billing_phone': billing_details['billing_phone'],
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
                content=(
                    f'Webhook received: {event["type"]} | Order already exists'
                ),
                status=200
            )
        else:
            # Get the cart from the event's metadata
            metadata = intent.metadata
            cart = metadata.cart
            shipping_cost = Decimal(metadata.shipping_cost)
            saving = Decimal(metadata.saving)

            # Get the Charge object for capturing of phone and email
            stripe_charge = stripe.Charge.retrieve(
                intent.latest_charge
            )

            # Get email from the charge object as it doesn't come in the intent
            billing_email = stripe_charge.billing_details.email
            billing_name = stripe_charge.billing_details.name
            billing_phone = stripe_charge.billing_details.phone

            billing_details = {
                'billing_name': billing_name,
                'billing_email': billing_email,
                'billing_phone': billing_phone,
            }

            # Split full name onto first and last name
            full_name = intent.shipping.name
            first_name = full_name.split()[0]
            last_name = (
                full_name.split()[-1] if len(full_name.split()) > 1 else "")

            phone = intent.shipping.phone
            street_address = intent.shipping.address.line1
            city = intent.shipping.address.city
            county = intent.shipping.address.state
            postal_code = intent.shipping.address.postal_code
            country = intent.shipping.address.country

            # Accurately converting to a Decimal
            grand_total = Decimal(stripe_charge.amount) / Decimal('100.00')
            order_total = grand_total + saving - shipping_cost

            try:
                order = Order(
                    first_name=first_name,
                    last_name=last_name,
                    email=billing_email,
                    phone_number=phone,
                    country=country,
                    postcode=postal_code,
                    town_city=city,
                    street_address=street_address,
                    county=county,
                    order_total=order_total,
                    delivery_cost=shipping_cost,
                    saving=saving,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order.save()
                # Create order line items
                for item_id, quantity in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    print(f'Webhook: {item_id} - {quantity}')
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )

                    order_line_item.save()

                # Send confirmation email
                self._send_confirmation_email(order, billing_details)

                return HttpResponse(
                    content=(
                        f'Webhook received: {event["type"]} | '
                        f'SUCCESS: Created order in webhook'
                    ),
                    status=200
                )

            except IntegrityError:
                return HttpResponse(
                    content=(
                        f'Webhook received: {event["type"]} | '
                        f'ERROR: Order already exists'
                    ),
                    status=200
                )
