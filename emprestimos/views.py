from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Emprestimo
from .forms import EmprestimoForm


class ListaEmprestimos(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'
    context_object_name = 'emprestimos'
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['pagina'] = 'emprestimos'
        return contexto


class CriarEmprestimo(CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos:list')


class EditarEmprestimo(UpdateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos:list')


class DeletarEmprestimo(DeleteView):
    model = Emprestimo
    template_name = 'emprestimo_confirm_delete.html'
    success_url = reverse_lazy('emprestimos:list')
