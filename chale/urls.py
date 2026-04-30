from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('clientes.urls')),
    path('', include('propriedades.urls')),
    path('', include('chaves.urls')),
    path('', include('emprestimos.urls')),
    path('', include('reservas.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
