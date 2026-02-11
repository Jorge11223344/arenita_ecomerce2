from django.urls import path
from . import views

urlpatterns = [
    path("webpay/init/<int:order_id>/", views.webpay_init, name="webpay_init"),
    path("webpay/return/", views.webpay_return, name="webpay_return"),
]
