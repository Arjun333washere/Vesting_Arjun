from django.urls import path

from .views import *

urlpatterns=[
    path('login/',login_view, name='login'),
    path('home/',home_view, name='home'),
    path('register/',RegisterView.as_view(), name='register'),


]
