from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Propriedade
from .forms import PropriedadeForm


class ListaPropriedades(ListView):
    model = Propriedade
    template_name = 'propriedades.html'
    context_object_name = 'propriedades'
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['pagina'] = 'propriedades'
        return contexto


class CriarPropriedade(CreateView):
    model = Propriedade
    form_class = PropriedadeForm
    template_name = 'propriedade_form.html'
    success_url = reverse_lazy('propriedades')


class EditarPropriedade(UpdateView):
    model = Propriedade
    form_class = PropriedadeForm
    template_name = 'propriedade_form.html'
    success_url = reverse_lazy('propriedades')

class DeletarPropriedade(DeleteView):
    model = Propriedade
    template_name = 'propriedade_confirm_delete.html'
    success_url = reverse_lazy('propriedades')
