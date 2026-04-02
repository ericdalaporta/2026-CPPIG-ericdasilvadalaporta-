from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Chave
from .forms import ChaveForm


class ListaChaves(ListView):
    model = Chave
    template_name = 'chaves.html'
    context_object_name = 'chaves'
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['pagina'] = 'chaves'
        return contexto


class CriarChave(CreateView):
    model = Chave
    form_class = ChaveForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves:list')


class EditarChave(UpdateView):
    model = Chave
    form_class = ChaveForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves:list')


class DeletarChave(DeleteView):
    model = Chave
    template_name = 'chave_confirm_delete.html'
    success_url = reverse_lazy('chaves:list')
