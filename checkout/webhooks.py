from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import WH_Handler

import stripe


@require_POST
@csrf_exempt
def webhook_view(request):
    """ Listen for webhooks from Stripe """

    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret,
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(content=e, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(content=e, status=400)
        # Set the generic error message for the webhook handler
    except Exception as e:
        return HttpResponse(content=e, status=400)

    handler = WH_Handler(request)

    # Handle the event
    if event and hasattr(event, 'type') and \
            event.type == 'payment_intent.succeeded':

        handler.handle_payment_intent_succeeded(event)

    return HttpResponse(status=200)
