from django.urls import path
from . import views


urlpatterns = [
    path('shipping/', views.checkout_shipping, name='checkout_shipping'),
]
