from django.urls import path
from . import views


urlpatterns = [
    path('shipping/', views.checkout_shipping, name='checkout_shipping'),
    path('payment/', views.checkout_payment, name='checkout_payment'),
    path('confirmation/', views.order_confirmation, name='order_confirmation'),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'),
    # path('wh/', webhook, name='webhook'),
]
