from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('propriedades/', include('propriedades.urls')),
    path('chaves/', include('chaves.urls')),
    path('reservas/', include('reservas.urls')),
    path('emprestimos/', include('emprestimos.urls')),
    path('registros/', include('registros.urls')),
]
