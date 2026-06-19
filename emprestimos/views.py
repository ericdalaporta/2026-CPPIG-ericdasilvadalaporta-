from datetime import date

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
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
from chaves.models import CopiaChave


# =============================================
# FUNÇÕES AUXILIARES
# =============================================

def atualizar_status_copias(emprestimo, novo_status):
    """Atualiza o status de todas as cópias do empréstimo."""

    for item in emprestimo.itens.all():
        item.copia_chave.status = novo_status
        item.copia_chave.save()


def criar_itens(emprestimo, copias_selecionadas):
    """Cria os itens e marca as cópias como emprestadas."""

    for copia_id in copias_selecionadas:
        copia = CopiaChave.objects.get(id=copia_id)

        ItemEmprestimo.objects.create(
            emprestimo=emprestimo,
            copia_chave=copia,
            status='EMPRESTADA'
        )

        copia.status = 'EMPRESTADA'
        copia.save()


def devolver_itens(emprestimo):
    """Devolve os itens e libera as cópias."""

    hoje = date.today()

    for item in emprestimo.itens.all():

        # Não altera uma data de devolução que já existia
        if item.data_devolucao_item is None:
            item.data_devolucao_item = hoje

        item.status = 'DEVOLVIDA'

        # Guarda a multa final daquele item
        item.multa = item.calcular_multa()

        item.copia_chave.status = 'DISPONIVEL'

        item.copia_chave.save()
        item.save()


# =============================================
# LISTAR EMPRÉSTIMOS
# =============================================

class EmprestimosView(PermissionRequiredMixin, ListView):

    model = Emprestimo
    template_name = 'emprestimos.html'
    paginate_by = 10
    permission_required = 'emprestimos.view_emprestimo'

    def get_queryset(self):
        termo_busca = self.request.GET.get('buscar')

        emprestimos = Emprestimo.objects.all().order_by('-id')

        if termo_busca:
            emprestimos = emprestimos.filter(
                Q(cliente__nome__icontains=termo_busca)
                | Q(id__icontains=termo_busca)
            )

        return emprestimos


# =============================================
# CRIAR EMPRÉSTIMO
# =============================================

class EmprestimoAddView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):

    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo criado com sucesso!'
    permission_required = 'emprestimos.add_emprestimo'

    def form_valid(self, form):
        copias_selecionadas = self.request.POST.getlist('copias')

        if not copias_selecionadas:
            form.add_error(
                None,
                'Selecione pelo menos uma cópia de chave.'
            )
            return self.form_invalid(form)

        form.instance.ativo = True 
        """isso eh para garantir que o emprestimo seja criado como ativo (em andamento)"""
        
        response = super().form_valid(form)

        criar_itens(
            self.object,
            copias_selecionadas
        )

        return response


# =============================================
# EDITAR EMPRÉSTIMO
# =============================================

class EmprestimoUpdateView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):

    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo atualizado com sucesso!'
    permission_required = 'emprestimos.change_emprestimo'

    def form_valid(self, form):

        copias_selecionadas = self.request.POST.getlist('copias')

        if not copias_selecionadas:
            form.add_error(
                None,
                'Selecione pelo menos uma cópia de chave.'
            )
            return self.form_invalid(form)

        # Libera as cópias antigas
        atualizar_status_copias(
            self.object,
            'DISPONIVEL'
        )

        # Remove os itens antigos
        self.object.itens.all().delete()

        # Salva as alterações do empréstimo
        response = super().form_valid(form)

        # Cria os novos itens
        criar_itens(
            self.object,
            copias_selecionadas
        )

        return response


# =============================================
# DELETAR EMPRÉSTIMO
# =============================================

class EmprestimoDeleteView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):

    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo apagado com sucesso!'
    permission_required = 'emprestimos.delete_emprestimo'

    def form_valid(self, form):

        # Libera as cópias antes de apagar
        atualizar_status_copias(
            self.object,
            'DISPONIVEL'
        )

        return super().form_valid(form)


# =============================================
# CONCLUIR EMPRÉSTIMO
# =============================================

class EmprestimoToggleDisponibilidadeView(
    PermissionRequiredMixin,
    View
):
    """
    O nome foi mantido para não quebrar a URL existente.

    Agora essa view apenas conclui o empréstimo.
    Ela não permite reativar o empréstimo.
    """

    permission_required = 'emprestimos.change_emprestimo'

    def post(self, request, pk):

        try:
            emprestimo = Emprestimo.objects.get(pk=pk)

            if not emprestimo.ativo:
                return JsonResponse({
                    'success': True,
                    'novo_status': 'Concluído',
                    'ativo': False,
                    'multa': emprestimo.calcular_multa()
                })

            # Guarda o dia em que a multa deve parar
            emprestimo.ativo = False
            emprestimo.data_conclusao = date.today()
            emprestimo.save()

            # Devolve as chaves
            devolver_itens(emprestimo)

            return JsonResponse({
                'success': True,
                'novo_status': 'Concluído',
                'ativo': False,
                'multa': emprestimo.calcular_multa()
            })

        except Emprestimo.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Empréstimo não encontrado.'
            }, status=404)

        except Exception as erro:
            return JsonResponse({
                'success': False,
                'error': str(erro)
            }, status=500)