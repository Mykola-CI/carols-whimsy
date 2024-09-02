from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_vendor_dashboard, name='view_dashboard'),
    path('product/add/', views.add_product, name='add_product'),
    path(
        'product/edit/<int:product_id>/',
        views.edit_product,
        name='edit_product'),
]
