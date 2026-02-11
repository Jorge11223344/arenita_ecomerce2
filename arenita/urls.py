from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('tienda/', include('shop.urls')),
    path('carro/', include('cart.urls')),
    path('checkout/', include('orders.urls')),  # <-- NUEVO
    path('', include('payments.urls')),  # ← agrega esta línea

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
