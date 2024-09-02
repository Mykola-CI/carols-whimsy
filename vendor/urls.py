from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_vendor_dashboard, name='view_dashboard'),

]
