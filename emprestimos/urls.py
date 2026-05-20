from django.urls import path

from .views import EmprestimosView, EmprestimoAddView, EmprestimoUpdateView, EmprestimoDeleteView, EmprestimoToggleStatusView, EmprestimoSalvarDevolucaoView

urlpatterns = [
    path('emprestimos', EmprestimosView.as_view(), name='emprestimos'),
    path('emprestimo/adicionar/', EmprestimoAddView.as_view(), name='emprestimo_adicionar'),
    path('<int:pk>/emprestimo/editar/', EmprestimoUpdateView.as_view(), name='emprestimo_editar'),
    path('<int:pk>/emprestimo/apagar/', EmprestimoDeleteView.as_view(), name='emprestimo_apagar'),
    path('<int:pk>/emprestimo/toggle-status/', EmprestimoToggleStatusView.as_view(), name='emprestimo_toggle_status'),
    path('<int:pk>/salvar-devolucao/', EmprestimoSalvarDevolucaoView.as_view(), name='salvar_devolucao'),
]
