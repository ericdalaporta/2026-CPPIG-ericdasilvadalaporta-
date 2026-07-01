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


# funções auxiliares

def atualizar_status_copias(emprestimo, novo_status):
    # atualiza o status de todas as cópias do empréstimo

    for item in emprestimo.itens.all():
        item.copia_chave.status = novo_status
        item.copia_chave.save()


def criar_itens(emprestimo, copias_selecionadas):
    # cria os itens e marca as cópias como emprestadas

    for copia_id in copias_selecionadas:
        copia = CopiaChave.objects.get(id=copia_id)

        ItemEmprestimo.objects.create(
            emprestimo=emprestimo,
            copia_chave=copia,
            status='EMPRESTADA'
        )

        copia.status = 'EMPRESTADA'
        copia.save()


def adicionar_copias_portao(copias_selecionadas):
    # adiciona uma cópia disponível dos portões associados

    ids_copias = list(copias_selecionadas)

    copias = CopiaChave.objects.filter(
        id__in=ids_copias
    ).select_related(
        'chave__propriedade__portao_associado'
    )

    for copia in copias:

        # se a cópia não estiver ligada a uma chave, vai para a próxima
        if copia.chave is None:
            continue

        propriedade = copia.chave.propriedade

        # se a chave não estiver ligada a uma propriedade, vai para a próxima
        if propriedade is None:
            continue

        # verifica se é um chalé exclusivo com portão associado
        if (
            propriedade.tipo == 'CHALE_EXCLUSIVO'
            and propriedade.portao_associado
        ):
            portao = propriedade.portao_associado

            # verifica se uma cópia desse portão já foi selecionada
            portao_ja_incluido = CopiaChave.objects.filter(
                id__in=ids_copias,
                chave__propriedade=portao
            ).exists()

            if portao_ja_incluido:
                continue

            # procura uma cópia disponível da chave do portão
            copia_portao = CopiaChave.objects.filter(
                chave__propriedade=portao,
                status='DISPONIVEL'
            ).first()

            # impede salvar caso não exista cópia disponível
            if copia_portao is None:
                raise ValueError(
                    f'Não existe uma cópia disponível da chave do portão {portao.nome}.'
                )

            # adiciona a cópia do portão na lista do empréstimo
            ids_copias.append(str(copia_portao.id))

    return ids_copias


def devolver_itens(emprestimo):
    # marca os itens como devolvidos e libera as cópias

    for item in emprestimo.itens.all():

        item.status = 'DEVOLVIDA'
        item.copia_chave.status = 'DISPONIVEL'

        item.copia_chave.save()
        item.save()


# listagem dos empréstimos

class EmprestimosView(PermissionRequiredMixin, ListView):

    model = Emprestimo
    template_name = 'emprestimos.html'
    paginate_by = 10
    permission_required = 'emprestimos.view_emprestimo'

    def get_queryset(self):
        termo_busca = self.request.GET.get('buscar')

        # pega todos os empréstimos e mostra os mais novos primeiro
        emprestimos = Emprestimo.objects.all().order_by('-id')

        # procura pelo nome do cliente ou pelo id do empréstimo
        if termo_busca:
            emprestimos = emprestimos.filter(
                Q(cliente__nome__icontains=termo_busca)
                | Q(id__icontains=termo_busca)
            )

        return emprestimos


# criação do empréstimo

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

        # pega as cópias selecionadas no formulário
        copias_selecionadas = self.request.POST.getlist('copias')

        # impede criar um empréstimo sem cópias
        if not copias_selecionadas:
            form.add_error(
                None,
                'Selecione pelo menos uma cópia de chave.'
            )

            return self.form_invalid(form)

        # verifica se o usuário marcou a opção de incluir o portão
        incluir_portao = self.request.POST.get('incluir_portao')

        if incluir_portao:
            try:
                copias_selecionadas = adicionar_copias_portao(
                    copias_selecionadas
                )

            except ValueError as erro:
                form.add_error(
                    None,
                    str(erro)
                )

                return self.form_invalid(form)

        # garante que o empréstimo seja criado como ativo
        form.instance.ativo = True

        # salva o empréstimo
        response = super().form_valid(form)

        # cria os itens com as cópias selecionadas
        criar_itens(
            self.object,
            copias_selecionadas
        )

        return response


# edição do empréstimo

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

        # pega as cópias selecionadas no formulário
        copias_selecionadas = self.request.POST.getlist('copias')

        # impede salvar sem selecionar alguma cópia
        if not copias_selecionadas:
            form.add_error(
                None,
                'Selecione pelo menos uma cópia de chave.'
            )

            return self.form_invalid(form)

        # verifica se o usuário marcou a opção de incluir o portão
        incluir_portao = self.request.POST.get('incluir_portao')

        if incluir_portao:
            try:
                copias_selecionadas = adicionar_copias_portao(
                    copias_selecionadas
                )

            except ValueError as erro:
                form.add_error(
                    None,
                    str(erro)
                )

                return self.form_invalid(form)

        # libera as cópias antigas
        atualizar_status_copias(
            self.object,
            'DISPONIVEL'
        )

        # remove os itens antigos
        self.object.itens.all().delete()

        # salva as alterações
        response = super().form_valid(form)

        # cria os itens novamente com as cópias escolhidas
        criar_itens(
            self.object,
            copias_selecionadas
        )

        return response


# exclusão do empréstimo

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

        # libera as cópias antes de apagar o empréstimo
        atualizar_status_copias(
            self.object,
            'DISPONIVEL'
        )

        return super().form_valid(form)


# conclusão do empréstimo

class EmprestimoToggleDisponibilidadeView(
    PermissionRequiredMixin,
    View
):

    # o nome foi mantido para não quebrar a url existente
    # essa view apenas conclui o empréstimo
    # ela não permite reativar um empréstimo concluído

    permission_required = 'emprestimos.change_emprestimo'

    def post(self, request, pk):

        try:
            # busca o empréstimo pelo id
            emprestimo = Emprestimo.objects.get(pk=pk)

            # se já estiver concluído, apenas retorna sucesso
            if not emprestimo.ativo:
                return JsonResponse({
                    'success': True,
                    'novo_status': 'Concluído',
                    'ativo': False,
                    'multa': emprestimo.calcular_multa()
                })

            # marca o empréstimo como concluído
            emprestimo.ativo = False

            # guarda a data em que a multa deve parar de aumentar
            emprestimo.data_conclusao = date.today()

            emprestimo.save()

            # devolve os itens e libera as cópias
            devolver_itens(emprestimo)

            return JsonResponse({
                'success': True,
                'novo_status': 'Concluído',
                'ativo': False,
                'multa': emprestimo.calcular_multa()
            })

        # acontece quando não existe empréstimo com esse id
        except Emprestimo.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Empréstimo não encontrado.'
            }, status=404)

        # captura qualquer outro erro
        except Exception as erro:
            return JsonResponse({
                'success': False,
                'error': str(erro)
            }, status=500)