from django.urls import path

from .views import (
    EmprestimosView,
    EmprestimoAddView,
    EmprestimoUpdateView,
    EmprestimoDeleteView,
    EmprestimoToggleDisponibilidadeView,
    ItemEmprestimoPerdidoView,
)

urlpatterns = [
    path('emprestimos', EmprestimosView.as_view(), name='emprestimos'),
    path('emprestimo/adicionar/', EmprestimoAddView.as_view(), name='emprestimo_adicionar'),
    path('<int:pk>/emprestimo/editar/', EmprestimoUpdateView.as_view(), name='emprestimo_editar'),
    path('<int:pk>/emprestimo/apagar/', EmprestimoDeleteView.as_view(), name='emprestimo_apagar'),
    path('<int:pk>/emprestimo/toggle-disponibilidade/', EmprestimoToggleDisponibilidadeView.as_view(), name='emprestimo_toggle_disponibilidade'),
    path('item-emprestimo/<int:pk>/perdido/', ItemEmprestimoPerdidoView.as_view(), name='item_emprestimo_perdido'),
]