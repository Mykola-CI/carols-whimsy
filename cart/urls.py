from django.urls import path
from . import views


urlpatterns = [
    path('summary/', views.cart_summary, name='cart_summary'),
    path('add/', views.add_to_cart, name='cart_add'),
    path('update/', views.update_cart, name='update_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path(
        'remove/item/<int:product_id>/',
        views.remove_item,
        name='remove_item'),
]
