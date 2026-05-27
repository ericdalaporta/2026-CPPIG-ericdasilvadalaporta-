from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Cliente
from .forms import ClienteModelForm


class ClientesView(ListView):
    
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'object_list'
    paginate_by = 10

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


def enviar_cobranca_chave_perdida(request, pk): # Envia email de cobrança por chave perdida
    """
    Envia email de cobrança ao cliente por chave perdida
    """
    # Busca o cliente no banco de dados pelo ID (pk)
    # Se não encontrar, retorna erro 404
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Cria uma lista com o email do cliente
    email = []
    email.append(cliente.email)
    
    # Prepara os dados que vão ser usados nos templates de email
    dados = {'cliente': cliente}
    
    # Renderiza o template de texto puro (arquivo .txt)
    texto_email = render_to_string('emails/texto_email.txt', dados)
    
    # Renderiza o template HTML (arquivo .html) com formatação bonita
    html_email = render_to_string('emails/texto_email.html', dados)
    
    # Envia o email para o cliente
    send_mail(
        subject='Cobrança por Chave Perdida - Chale',  # Assunto do email
        message=texto_email,  # Corpo do email em texto puro
        from_email='ericdasilvadalaporta@gmail.com',  # Email de origem
        recipient_list=email,  # Lista de destinatários
        html_message=html_email,  # Versão HTML do email
        fail_silently=False,  # Se False, mostra erro caso falhe
    )
    
    # Mostra mensagem de sucesso ao usuário
    messages.success(request, f'Email de cobrança enviado para {cliente.email}')
    
    # Redireciona de volta para a lista de clientes
    return redirect('clientes')