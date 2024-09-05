from django.urls import path
from . import views


urlpatterns = [
     path('', views.view_user_profile, name='view_profile'),
     path(
          'update/basic_info',
          views.update_user_basic_info,
          name='update_basic_info'),
     path('update/phone', views.update_user_phone, name='update_phone'),
     path('update/email', views.change_email, name='update_email'),
     path('update/password', views.change_password, name='change_password'),
     path('order_history', views.view_order_history, name='order_history'),
     path('user_account/delete/',
          views.delete_user_account, name='delete_account'),
     path('shipping_addresses/', views.set_shipping_details_profile,
          name='manage_shipping_addresses'),
     path('shipping_addresses/edit/<int:address_id>/',
          views.edit_shipping_addresses_profile,
          name='edit_shipping_addresses'),
     path('get_address_data/', views.get_address_data, name='get_address_data'),
     path(
          'delete_address/<int:address_id>/',
          views.delete_address, name='delete_address'),
     path('wishlist/', views.wishlist_view, name='wishlist'),
]
