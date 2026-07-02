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

def atualizar_status_copias(emprestimo): 
    # essa funcao eh chamada dentro das views de update e delete do emprestimo
    # serve pra mudar o status de todas as cópias ligadas a um empréstimo
    # libera as cópias quando o empréstimo é atualizado ou apagado
    # a função recebe o empréstimo usado

    for item in emprestimo.itens.all():  # pega um item de cada vez
        item.copia_chave.status = 'DISPONIVEL'  # deixa a cópia disponível
        item.copia_chave.save()  # salva a mudança no banco


def criar_itens(emprestimo, copias_selecionadas):
    # essa funcao vai ser chamada dentro das views de add e update do emprestimo
    # serve pra ligar as copias selecionadas ao emprestimo e marca-las como emprestadas
    # o ItemEmprestimo registrea qual copia de chave está dentro de qual empréstimo
    # exemplo: emprestimo 10 tem copia 3 e 7, na tabela ItemEmprestimo vai ter duas linhas
    # uma com emprestimo=10 e copia=3, outra com emprestimo=10 e copia=7

    for copia_id in copias_selecionadas: # p cada id de copia que foi selecionado
        copia = CopiaChave.objects.get(id=copia_id) # busca no banco a copia com aquele id e guarda na var copia

        ItemEmprestimo.objects.create(
            emprestimo=emprestimo,
            copia_chave=copia,
            status='EMPRESTADA'
        ) # cria o registro na tabela ItemEmprestimo, ligando a copia ao emprestimo

        copia.status = 'EMPRESTADA'
        copia.save() 


def adicionar_copias_portao(copias_selecionadas): 
    # essa funcao recebe a lista copias_selecionadas, ve se alguma copia pertence a um chale exclusivo
    # e se pertencer, procura uma copia disponivel do portao associado e coloca o id dela na mesma lista
    ids_copias = list(copias_selecionadas) # cria uma lista com os ids das copias selecionadas, pra poder add a copia do portão se for o caso

    # busca as cópias com esses ids no banco de dados
    copias = CopiaChave.objects.filter(id__in=ids_copias)

    for copia in copias: # analisa uma copia por vez pra ver se pertence a chale exclusivo
        propriedade = copia.chave.propriedade # pega a propriedade ligada na copia pra ver se é um chalé exclusivo com portão

        # verifica se a cópia pertence a um chalé exclusivo com portão
        if propriedade.tipo == 'CHALE_EXCLUSIVO' and propriedade.portao_associado:
            portao = propriedade.portao_associado # variavel portão recebe o portão associado ao chalé exclusivo

            # verifica se as copias selecionadas já incluem a copia do portao
            portao_ja_incluido = CopiaChave.objects.filter(
                id__in=ids_copias, # pega os ids das copias selecionadas
                chave__propriedade=portao # verifica se a copia do portao já tá na lista das copias selecionadas
            ).exists() # se sim, portao_ja_incluido recebe True, se não, recebe False

            if not portao_ja_incluido: # se ainda n tem uma copia do portao na lista
                copia_portao = CopiaChave.objects.filter( # procure copias que pertençam ao portao que estejam disponiveis
                    chave__propriedade=portao,
                    status='DISPONIVEL'
                ).first() # pra pegar a primeira encontrada

                if copia_portao is None: 
                    return None

                # pega o ID da copia do portao e add na lista de cópias selecionadas
                ids_copias.append(str(copia_portao.id))

    return ids_copias


def pegar_copias_selecionadas(request, form):
    # pega todas as cópias selecionadas no formulário

    copias_selecionadas = request.POST.getlist('copias')

    # impede salvar um empréstimo sem cópias
    if not copias_selecionadas:
        form.add_error(
            None,
            'Selecione pelo menos uma cópia de chave.'
        )

        return None

    # verifica se o usuário marcou a opção de incluir o portão
    incluir_portao = request.POST.get('incluir_portao') # pega o checkbox do formulario chamado incluir portao

    if incluir_portao: # se marcou incluir portao, chama adicionar_copias_portao pra add a copia do portao se for um chale exclusivo com portao
        copias_selecionadas = adicionar_copias_portao(copias_selecionadas)

        if copias_selecionadas is None: # se a função adicionar_copias_portao retornar None, eh pq nao tem copia disponivel do portao entao da erro
            form.add_error(
                None,
                'Não existe uma cópia disponível da chave do portão.'
            )
            return None

    return copias_selecionadas


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

        emprestimos = Emprestimo.objects.all()

        if termo_busca:
            emprestimos = emprestimos.filter(
                cliente__nome__icontains=termo_busca
            )

        return emprestimos

# criação do empréstimo

class EmprestimoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo criado com sucesso!'
    permission_required = 'emprestimos.add_emprestimo'

    def form_valid(self, form):

        # pega e verifica as cópias selecionadas
        copias_selecionadas = pegar_copias_selecionadas(
            self.request,
            form
        )

        # volta para o formulário caso exista algum erro
        if copias_selecionadas is None:
            return self.form_invalid(form)

        # garante que o empréstimo seja criado como ativo (em andamento)
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

class EmprestimoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo atualizado com sucesso!'
    permission_required = 'emprestimos.change_emprestimo'

    def form_valid(self, form):

        # pega e verifica as cópias selecionadas
        copias_selecionadas = pegar_copias_selecionadas(
            self.request,
            form
        )

        # volta para o formulário caso exista algum erro
        if copias_selecionadas is None:
            return self.form_invalid(form)

        # libera as cópias antigas
        atualizar_status_copias(self.object)

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

class EmprestimoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):

    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo apagado com sucesso!'
    permission_required = 'emprestimos.delete_emprestimo'

    def form_valid(self, form):

        # libera as cópias antes de apagar o empréstimo
        atualizar_status_copias(self.object)

        return super().form_valid(form)


from django.shortcuts import get_object_or_404


class EmprestimoToggleDisponibilidadeView(PermissionRequiredMixin, View): # toggle eh o botaozinho pra alternar os estados

    permission_required = 'emprestimos.change_emprestimo'

    def post(self, request, pk): # metodo pra quando o usuario clicar no botao de alternar status
        # manda pro servidor um POST com o id do emprestimo, e o servidor vai alternar o status do emprestimo

        emprestimo = get_object_or_404(Emprestimo, pk=pk) # pega o emprestimo com o id passado na url, se nao achar, retorna 404

        if emprestimo.ativo:
            emprestimo.ativo = False  # muda de ativo pra concluido o emprestimo
            emprestimo.data_conclusao = date.today()
            emprestimo.save()

            devolver_itens(emprestimo) # chama la de cima pra liberar chaves copias

        return JsonResponse({ # devolve uma resposta pro javascript que chamou essa view, dizendo que deu certo e qual o novo status do emprestimo
            'success': True,
            'novo_status': 'Concluído',
            'ativo': False,
            'multa': emprestimo.calcular_multa()
        })