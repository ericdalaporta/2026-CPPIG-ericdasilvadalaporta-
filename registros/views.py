from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Registro
from .forms import RegistroForm


class ListaRegistros(ListView):
    model = Registro
    template_name = 'registros.html'
    context_object_name = 'registros'
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['pagina'] = 'registros'
        return contexto


class CriarRegistro(CreateView):
    model = Registro
    form_class = RegistroForm
    template_name = 'registro_form.html'
    success_url = reverse_lazy('registros:list')


class EditarRegistro(UpdateView):
    model = Registro
    form_class = RegistroForm
    template_name = 'registro_form.html'
    success_url = reverse_lazy('registros:list')


class DeletarRegistro(DeleteView):
    model = Registro
    template_name = 'registro_confirm_delete.html'
    success_url = reverse_lazy('registros:list')
