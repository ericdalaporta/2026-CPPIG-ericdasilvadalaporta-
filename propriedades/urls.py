from django.urls import path
from .views import ListaPropriedades, CriarPropriedade, EditarPropriedade, DeletarPropriedade

app_name = 'propriedades'

urlpatterns = [
    path('', ListaPropriedades.as_view(), name='list'),
    path('criar/', CriarPropriedade.as_view(), name='create'),
    path('<int:pk>/editar/', EditarPropriedade.as_view(), name='update'),
    path('<int:pk>/deletar/', DeletarPropriedade.as_view(), name='delete'),
]
