from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_dashboard, name='view_dashboard'),

]
