from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_owner/', views.get_owner, name='get_owner'),
    path('add_beneficiary/', views.add_beneficiary, name='add_beneficiary'),
]

