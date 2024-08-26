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
]
