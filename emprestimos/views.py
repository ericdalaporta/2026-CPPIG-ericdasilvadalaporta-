from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)

from .forms import EmprestimoModelForm
from .models import Emprestimo, ItemEmprestimo
from .services import (
    RegraEmprestimoError,
    atualizar_emprestimo,
    cancelar_emprestimo,
    concluir_emprestimo,
    criar_emprestimo,
    marcar_item_como_perdido,
)


def adicionar_erros_do_service_no_form(form, erro):
    mensagens = getattr(erro, 'messages', None) or [str(erro)]

    for mensagem in mensagens:
        form.add_error(None, mensagem)


class EmprestimosView(PermissionRequiredMixin, ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'
    paginate_by = 10
    permission_required = 'emprestimos.view_emprestimo'

    def get_queryset(self):
        termo_busca = self.request.GET.get('buscar')

        emprestimos = Emprestimo.objects.select_related('cliente').prefetch_related(
            'itens__copia_chave__chave'
        ).order_by('-id')

        if termo_busca:
            emprestimos = emprestimos.filter(
                cliente__nome__icontains=termo_busca
            )

        return emprestimos


class EmprestimoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo criado com sucesso!'
    permission_required = 'emprestimos.add_emprestimo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['copias_selecionadas'] = []
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['copias_selecionadas'] = self.request.POST.getlist('copias')
        return self.render_to_response(context)

    def form_valid(self, form):
        emprestimo = form.save(commit=False)
        ids_copias = self.request.POST.getlist('copias')
        incluir_portao = bool(self.request.POST.get('incluir_portao'))

        try:
            self.object = criar_emprestimo(
                emprestimo,
                ids_copias,
                incluir_portao=incluir_portao
            )
        except (RegraEmprestimoError, ValidationError) as erro:
            adicionar_erros_do_service_no_form(form, erro)
            return self.form_invalid(form)

        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())


class EmprestimoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo atualizado com sucesso!'
    permission_required = 'emprestimos.change_emprestimo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            context['copias_selecionadas'] = self.request.POST.getlist('copias')
        else:
            context['copias_selecionadas'] = [
                str(id_copia)
                for id_copia in self.object.itens.values_list('copia_chave_id', flat=True)
            ]

        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['copias_selecionadas'] = self.request.POST.getlist('copias')
        return self.render_to_response(context)

    def form_valid(self, form):
        emprestimo = form.save(commit=False)
        ids_copias = self.request.POST.getlist('copias')
        incluir_portao = bool(self.request.POST.get('incluir_portao'))

        try:
            self.object = atualizar_emprestimo(
                emprestimo,
                ids_copias,
                incluir_portao=incluir_portao
            )
        except (RegraEmprestimoError, ValidationError) as erro:
            adicionar_erros_do_service_no_form(form, erro)
            return self.form_invalid(form)

        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())


class EmprestimoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo cancelado com sucesso! O histórico foi preservado.'
    permission_required = 'emprestimos.delete_emprestimo'

    def form_valid(self, form):
        try:
            cancelar_emprestimo(self.object)
            messages.success(self.request, self.success_message)
        except (RegraEmprestimoError, ValidationError) as erro:
            mensagens = getattr(erro, 'messages', [str(erro)])

            for mensagem in mensagens:
                messages.error(self.request, mensagem)

        return redirect(self.success_url)


class EmprestimoToggleDisponibilidadeView(PermissionRequiredMixin, View):
    permission_required = 'emprestimos.change_emprestimo'

    def post(self, request, pk):
        emprestimo = get_object_or_404(Emprestimo, pk=pk)

        try:
            emprestimo = concluir_emprestimo(emprestimo)
        except (RegraEmprestimoError, ValidationError) as erro:
            mensagens = getattr(erro, 'messages', [str(erro)])

            return JsonResponse({
                'success': False,
                'error': ' '.join(mensagens)
            }, status=400)
        except Exception as erro:
            return JsonResponse({
                'success': False,
                'error': f'Erro interno ao concluir empréstimo: {erro}'
            }, status=500)

        return JsonResponse({
            'success': True,
            'novo_status': emprestimo.get_status(),
            'ativo': False,
            'multa': str(emprestimo.calcular_multa()),
            'atraso': emprestimo.get_atraso_formatado(),
        })


class ItemEmprestimoPerdidoView(PermissionRequiredMixin, View):
    permission_required = 'emprestimos.change_itememprestimo'

    def post(self, request, pk):
        item = get_object_or_404(ItemEmprestimo, pk=pk)
        observacao = request.POST.get('observacao', '')

        try:
            item = marcar_item_como_perdido(item, observacao=observacao)
        except (RegraEmprestimoError, ValidationError) as erro:
            mensagens = getattr(erro, 'messages', [str(erro)])

            return JsonResponse({
                'success': False,
                'error': ' '.join(mensagens)
            }, status=400)
        except Exception as erro:
            return JsonResponse({
                'success': False,
                'error': f'Erro interno ao marcar cópia como perdida: {erro}'
            }, status=500)

        return JsonResponse({
            'success': True,
            'status_item': item.status,
            'status_copia': item.copia_chave.status,
            'valor_cobranca_perda': str(item.valor_cobranca_perda),
        })