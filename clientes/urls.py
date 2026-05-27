from django.urls import path

from .views import ClientesView, ClienteAddView, ClienteUpdateView, ClienteDeleteView, enviar_cobranca_chave_perdida

urlpatterns = [
    path('clientes', ClientesView.as_view(), name='clientes'),
    path('cliente/adicionar/', ClienteAddView.as_view(), name='cliente_adicionar'),
    path('<int:pk>/cliente/editar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('<int:pk>/cliente/apagar/', ClienteDeleteView.as_view(), name='cliente_apagar'),
    path('<int:pk>/cliente/cobranca-chave-perdida/', enviar_cobranca_chave_perdida, name='cobranca_chave_perdida'),
]