from django.urls import path
from .views import ListaEmprestimos, CriarEmprestimo, EditarEmprestimo, DeletarEmprestimo

app_name = 'emprestimos'

urlpatterns = [
    path('', ListaEmprestimos.as_view(), name='list'),
    path('criar/', CriarEmprestimo.as_view(), name='create'),
    path('<int:pk>/editar/', EditarEmprestimo.as_view(), name='update'),
    path('<int:pk>/deletar/', DeletarEmprestimo.as_view(), name='delete'),
]
