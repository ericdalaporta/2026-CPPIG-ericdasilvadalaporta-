from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.core.paginator import Paginator
from django.contrib import messages

from .models import Cliente
from .forms import ClienteModelForm


class ClientesView(ListView):
    model = Cliente
    template_name = 'clientes.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            page = self.request.GET.get('page')
            return paginator.get_page(page)
        else:
            messages.info(self.request, 'Não existem clientes cadastrados!')
            return qs


class ClienteAddView(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente adicionado com sucesso!'


class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente alterado com sucesso!'




class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente apagado com sucesso!'
