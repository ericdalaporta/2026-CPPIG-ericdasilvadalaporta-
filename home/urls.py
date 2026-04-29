from django.urls import path

from clientes.views import ClientesView
from .views import IndexView
from clientes.views import ClientesView, ClienteAddView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cliente/adicionar/', ClienteAddView.as_view(), name='cliente_adicionar'),
]