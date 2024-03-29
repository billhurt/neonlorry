import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from orders.models import Order

from basket.basket import Basket
from orders.views import payment_confirmation


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')

class Error(TemplateView):
    template_name = 'payment/error.html'

@login_required
def BasketView(request):

    basket = Basket(request)
    # Stripe only accepts integers. Convert decimalised value to string, and replace the '.' with ''
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = 'sk_test_51O9YfHKYG9KhsX3JktqjsiWqraOLp9Ss4aLibmafyTqr24qJOhI7Wt1R1V7rVRFVICIVTSkwdm7y6zccajxGBI2A00vGuUAeer'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/payment_form.html', {'client_secret': intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
        
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)