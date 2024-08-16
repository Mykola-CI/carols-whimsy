from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .forms import OrderForm


def checkout_shipping(request):
    """ A view to return the index page """

    cart = Cart(request)
    if not cart:
        messages.error(request, "There's nothing in your Cart at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout-shipping.html'

    context = {
        'order_form': order_form,
    }

    return render(request, template, context)
