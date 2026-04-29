from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Cliente
from .forms import ClienteModelForm


class ClientesView(ListView):
    model = Cliente
    template_name = 'clientes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)
        return qs


class ClienteAddView(CreateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')