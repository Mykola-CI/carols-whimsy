from django.urls import path
from . import views


urlpatterns = [
    path('shipping/', views.checkout_shipping, name='checkout_shipping'),
    path('payment/', views.checkout_payment, name='checkout_payment'),
]
