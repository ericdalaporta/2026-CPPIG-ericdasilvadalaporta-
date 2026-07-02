import email

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models.deletion import ProtectedError

from .models import Cliente
from .forms import ClienteModelForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class ClientesView(PermissionRequiredMixin, ListView):
    
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'object_list'
    paginate_by = 10
    permission_required = 'clientes.view_cliente'

    def get_queryset(self): #filtra a lista de clientes
        
        buscar = self.request.GET.get('buscar')
        qs = Cliente.objects.all()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        return qs

    def get_context_data(self, **kwargs): #exibe mensagem caso n retorne nada
  
        context = super().get_context_data(**kwargs)
        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(self.request, 'Não existem clientes cadastrados com esse nome!')
        return context


class ClienteAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente adicionado com sucesso!'
    permission_required = 'clientes.add_cliente'


class ClienteUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
   
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente alterado com sucesso!'
    permission_required = 'clientes.change_cliente'


class ClienteDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):

    model = Cliente
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente apagado com sucesso'
    permission_required = 'clientes.delete_cliente'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)

        except ProtectedError:
            messages.error(
                request,
                'Não é possível apagar este cliente porque ele possui empréstimos ou reservas vinculados.'
            )

            return redirect('clientes')


def enviar_cobranca_chave_perdida(request, pk): # manda email de cobrança por chave perdida

    # busca cliente pelo id
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # cria uma lista com o email do cliente porque o send_email espera uma lista (mesmo que seja só um email)
    email = []
    email.append(cliente.email)
    
    # Prepara os dados que vão ser usados nos templates de email
    dados = {'cliente': cliente}
    
    # renderiza o template de texto puro ou em html bonitao, depende do app do usuario
    texto_email = render_to_string('emails/texto_email.txt', dados)
    html_email = render_to_string('emails/texto_email.html', dados)
    

    send_mail(
        subject='Cobrança por Chave Perdida - Chale',  
        message=texto_email,  
        from_email='ericdasilvadalaporta@gmail.com',
        recipient_list=email,  
        html_message=html_email, 
        fail_silently=False,  # se False, mostra erro caso falhe
    )
    
    # mostra mensagem de sucesso ao usuário
    messages.success(request, f'Email de cobrança enviado para {cliente.email}')
    
    # redireciona de volta para a lista de clientes
    return redirect('clientes')