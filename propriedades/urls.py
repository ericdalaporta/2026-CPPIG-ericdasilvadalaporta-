from django.urls import path
from .views import ListaPropriedades, CriarPropriedade, EditarPropriedade, DeletarPropriedade

urlpatterns = [
    path('propriedade', ListaPropriedades.as_view(), name='propriedades'),
    path('propriedade/criar', CriarPropriedade.as_view(), name='create'),
    path('<int:pk>/propriedade/editar', EditarPropriedade.as_view(), name='update'),
    path('<int:pk>/propriedade/deletar', DeletarPropriedade.as_view(), name='delete'),
]
