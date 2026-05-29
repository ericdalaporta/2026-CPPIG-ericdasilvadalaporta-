from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from datetime import date
from .models import Emprestimo, ItemEmprestimo
from .forms import EmprestimoModelForm
from chaves.models import CopiaChave
from django.contrib.auth.mixins import PermissionRequiredMixin


# =============================================
# FUNÇÕES AUXILIARES - Gerenciam cópias de chave
# =============================================

def atualizar_status_copias(emprestimo, novo_status): # atualiza o status de todas as cópias de um empréstimo (DISPONIVEL ou EMPRESTADA)
   
    for item in emprestimo.itens.all():
        item.copia_chave.status = novo_status
        item.copia_chave.save()

def criar_itens(emprestimo, copias_selecionadas): # cria os itens de empréstimo e marca as cópias como EMPRESTADA
    
    for copia_id in copias_selecionadas:
        copia = CopiaChave.objects.get(id=copia_id)
        
        # Cria a ligação empréstimo <-> cópia
        ItemEmprestimo.objects.create(
            emprestimo=emprestimo,
            copia_chave=copia,
            status='EMPRESTADA'
        )
        
        # Marca a cópia como emprestada
        copia.status = 'EMPRESTADA'
        copia.save()


def devolver_itens(emprestimo): # marca todos os itens como devolvidos e libera as cópias (DISPONIVEL)

    for item in emprestimo.itens.all():
        item.status = 'DEVOLVIDA'
        item.data_devolucao_item = date.today()
        item.copia_chave.status = 'DISPONIVEL'
        
        item.copia_chave.save()
        item.save()


# =============================================
# LISTAR - Mostra todos os empréstimos
# =============================================

class EmprestimosView(PermissionRequiredMixin, ListView): # mostra a lista de emprréstimos com opção de busca por cliente ou id
    """Exibe a lista de empréstimos com opção de busca."""
    
    model = Emprestimo
    template_name = 'emprestimos.html'
    paginate_by = 10

    def get_queryset(self):
        """Filtra empréstimos por cliente ou ID."""
        termo_busca = self.request.GET.get('buscar')
        
        emprestimos = Emprestimo.objects.all()
        
        if termo_busca:
            # Busca por nome do cliente OU ID do empréstimo
            emprestimos = emprestimos.filter(
                Q(cliente__nome__icontains=termo_busca) |
                Q(id__icontains=termo_busca)
            )
        
        return emprestimos
    
    permission_required = 'emprestimos.view_emprestimo'


# =============================================
# CRIAR - Novo empréstimo
# =============================================

class EmprestimoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo criado com sucesso!'
    permission_required = 'emprestimos.add_emprestimo'

    def form_valid(self, form):
        response = super().form_valid(form)
        
        copias_selecionadas = self.request.POST.getlist('copias')
        
        criar_itens(self.object, copias_selecionadas)
        
        return response


# =============================================
# EDITAR - Modifica um empréstimo
# =============================================

class EmprestimoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo atualizado com sucesso!'
    permission_required = 'emprestimos.change_emprestimo'
    def form_valid(self, form):

        # Libera cópias antigas
        atualizar_status_copias(self.object, 'DISPONIVEL')
        
        # Remove itens antigos
        self.object.itens.all().delete()
        
        # Salva formulário
        response = super().form_valid(form)
        
        # Cria novos itens
        copias_selecionadas = self.request.POST.getlist('copias')
        criar_itens(self.object, copias_selecionadas)
        
        return response


# =============================================
# DELETAR - Remove um empréstimo
# =============================================

class EmprestimoDeleteView(PermissionRequiredMixin, DeleteView):

    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')
    permission_required = 'emprestimos.delete_emprestimo'

    def delete(self, request, *args, **kwargs):
        
        # Libera cópias antes de deletar
        emprestimo = self.get_object()
        
        # Libera todas as cópias
        atualizar_status_copias(emprestimo, 'DISPONIVEL')
        
        # Deleta o empréstimo
        return super().delete(request, *args, **kwargs)


# =============================================
# TOGGLE - Alterna entre OCUPADO e DISPONÍVEL
# =============================================

class EmprestimoToggleDisponibilidadeView(PermissionRequiredMixin, View): # clicar no badge de status pra ir de ocupado pra disponivel (copias liberadas)
  
    permission_required = 'emprestimos.change_emprestimo'
    #Feito via AJAX (sem recarregar a página).

    def post(self, request, pk): # altera o status do emprestimo

        try:
            emprestimo = Emprestimo.objects.get(pk=pk)
            
            # Pega o novo status (true = ocupado, false = disponível)
            novo_status_ativo = request.POST.get('ativo') == 'true'
            
            # Atualiza o status do empréstimo
            emprestimo.ativo = novo_status_ativo
            emprestimo.save()

            # Atualiza as cópias de chave
            if novo_status_ativo:
                # Reativar: marca como EMPRESTADA
                atualizar_status_copias(emprestimo, 'EMPRESTADA')
            else:
                # Finalizar: devolve todos os itens e libera cópias
                devolver_itens(emprestimo)

            # Retorna sucesso com o novo status
            texto_status = 'Ocupado' if novo_status_ativo else 'Disponível'
            
            return JsonResponse({
                'success': True,
                'novo_status': texto_status,
                'ativo': novo_status_ativo
            })
            
        except Emprestimo.DoesNotExist:
            return JsonResponse(
                {'success': False, 'error': 'Empréstimo não encontrado'},
                status=404
            )
        except Exception as erro:
            return JsonResponse(
                {'success': False, 'error': str(erro)},
                status=500
            )