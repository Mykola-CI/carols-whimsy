from django.urls import path
from . import views
from .webhooks import webhook_view


urlpatterns = [
    path('shipping/', views.checkout_shipping, name='checkout_shipping'),
    path('payment/', views.checkout_payment, name='checkout_payment'),
    path(
        'confirmation/<order_number>/',
        views.order_confirmation,
        name='order_confirmation'),
    # path('success/<order_number>/', views.checkout_success, name='payment_success'),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'),
    path('wh/', webhook_view, name='webhook'),
    path(
        'order_pending/<str:pid>/', views.order_pending, name='order_pending'),
    path(
        'order_pending/<str:pid>/status/',
        views.check_order_status, name='check_order_status'),
    # path('order_interruption/',
    #      views.order_interruption,
    #      name='order_interruption'),
]
