import json
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

    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
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
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        handler.handle_payment_intent_succeeded(payment_intent)

    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object
        handler.handle_payment_intent_failed(payment_intent)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
