
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib import messages

from .models import Cliente
from .forms import ClienteModelForm


class ClientesView(ListView):
    
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        """Busca clientes, filtrando se user digitou nome"""
        buscar = self.request.GET.get('buscar')
        qs = Cliente.objects.all()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        return qs

    def get_context_data(self, **kwargs):
        """Mostra mensagem se busca não achou nada"""
        context = super().get_context_data(**kwargs)
        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(self.request, 'Não existem clientes cadastrados com esse nome!')
        return context


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


class ClienteDeleteView(SuccessMessageMixin, DeleteView):

    
    model = Cliente
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente apagado com sucesso'