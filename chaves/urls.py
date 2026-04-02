from django.urls import path
from .views import ListaChaves, CriarChave, EditarChave, DeletarChave

app_name = 'chaves'

urlpatterns = [
    path('', ListaChaves.as_view(), name='list'),
    path('criar/', CriarChave.as_view(), name='create'),
    path('<int:pk>/editar/', EditarChave.as_view(), name='update'),
    path('<int:pk>/deletar/', DeletarChave.as_view(), name='delete'),
]
