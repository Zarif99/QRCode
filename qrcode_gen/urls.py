from django.urls import path
from .views import index, invoice

urlpatterns = [
    path('', index, name='user_list_url'),
    path('customer/<str:slug>', invoice, name='customer_detail')
]
