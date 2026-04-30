from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator
from django.contrib import messages

from .models import Emprestimo
from .forms import EmprestimoModelForm


class EmprestimosView(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        qs = Emprestimo.objects.all()
        return qs

class EmprestimoAddView(SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo adicionado com sucesso!'


class EmprestimoUpdateView(SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo alterado com sucesso!'


class EmprestimoDeleteView(SuccessMessageMixin, DeleteView):
    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')
    
    def get_success_message(self, cleaned_data):
        emprestimo = self.object
        return f'Empréstimo "{emprestimo.id}" foi deletado com sucesso!'


class EmprestimoToggleStatusView(View):
    def get(self, request, pk):
        emprestimo = Emprestimo.objects.get(pk=pk)
        emprestimo.toggle_status()
        messages.success(request, f'Empréstimo alterado para: {emprestimo.get_status()}')
        return HttpResponseRedirect(reverse_lazy('emprestimos'))
