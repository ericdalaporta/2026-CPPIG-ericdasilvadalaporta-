from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('home.urls')),
    path('', include('propriedades.urls')),
    path('', include('chaves.urls')),
    path('', include('reservas.urls')),
    path('', include('emprestimos.urls')),
    path('', include('registros.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
