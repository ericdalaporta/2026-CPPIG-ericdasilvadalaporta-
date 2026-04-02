from django.urls import path
from .views import ListaRegistros, CriarRegistro, EditarRegistro, DeletarRegistro

app_name = 'registros'

urlpatterns = [
    path('', ListaRegistros.as_view(), name='list'),
    path('criar/', CriarRegistro.as_view(), name='create'),
    path('<int:pk>/editar/', EditarRegistro.as_view(), name='update'),
    path('<int:pk>/deletar/', DeletarRegistro.as_view(), name='delete'),
]
