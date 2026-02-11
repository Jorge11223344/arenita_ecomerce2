from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name='tienda'),
    path('categoria/<slug:categoria_slug>/', views.tienda, name='tienda_categoria'),
    path('producto/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
]
