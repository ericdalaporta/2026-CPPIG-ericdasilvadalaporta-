from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Sum
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from emprestimos.models import Emprestimo, ItemEmprestimo
from .forms import ClienteModelForm
from .models import Cliente


class ClientesView(PermissionRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'object_list'
    paginate_by = 10
    permission_required = 'clientes.view_cliente'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = Cliente.objects.all()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        return qs

    def get_context_data(self, **kwargs):
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


def enviar_cobranca_chave_perdida(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    itens_em_aberto = ItemEmprestimo.objects.select_related(
        'copia_chave__chave',
        'emprestimo'
    ).filter(
        emprestimo__cliente=cliente,
        emprestimo__status=Emprestimo.STATUS_EM_ANDAMENTO,
        status=ItemEmprestimo.STATUS_EMPRESTADA
    )

    if not itens_em_aberto.exists():
        messages.error(
            request,
            'Este cliente não possui cópias emprestadas em aberto para cobrança de perda.'
        )
        return redirect('clientes')

    valor_total = sum(item.copia_chave.valor_restituicao for item in itens_em_aberto)

    dados = {
        'cliente': cliente,
        'itens': itens_em_aberto,
        'valor_total': valor_total,
    }

    texto_email = render_to_string('emails/texto_email.txt', dados)
    html_email = render_to_string('emails/texto_email.html', dados)

    send_mail(
        subject='Cobrança por Chave Perdida - Chale',
        message=texto_email,
        from_email='ericdasilvadalaporta@gmail.com',
        recipient_list=[cliente.email],
        html_message=html_email,
        fail_silently=False,
    )

    messages.success(request, f'Email de cobrança enviado para {cliente.email}')
    return redirect('clientes')
