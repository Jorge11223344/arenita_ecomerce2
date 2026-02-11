from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('pagar/<int:order_id>/', views.pay, name='orders_pay'),
]
