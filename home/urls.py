from django.urls import path
from .views import index, reservas, emprestimos, registros, propriedades, chaves, notificacoes, usuarios, acessos

urlpatterns = [
    path('', index, name='index'),
    path('propriedades/', propriedades, name='propriedades'),
    path('chaves/', chaves, name='chaves'),
    path('usuarios/', usuarios, name='usuarios'),
    path('acessos/', acessos, name='acessos'),
    path('reservas/', reservas, name='reservas'),
    path('emprestimos/', emprestimos, name='emprestimos'),
    path('registros/', registros, name='registros'),
    path('notificacoes/', notificacoes, name='notificacoes'),
]