from django.urls import path
from . import views


urlpatterns = [
    path('summary/', views.cart_summary, name='cart_summary'),
    path('add/', views.add_to_cart, name='cart_add'),
    path('update/', views.cart_update, name='cart_update'),
    path('remove/', views.cart_remove, name='cart_remove'),
]
