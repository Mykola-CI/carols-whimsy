from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_user_profile, name='view_profile'),
    path(
        'update/basic_info',
        views.update_user_basic_info,
        name='update_basic_info'),
    path('update/contact', views.update_user_contact, name='update_contact'),
]
