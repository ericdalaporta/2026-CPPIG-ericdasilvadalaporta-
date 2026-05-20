from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json

from .models import Emprestimo, ItemEmprestimo
from .forms import EmprestimoModelForm
from chaves.models import CopiaChave


class EmprestimosView(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = Emprestimo.objects.all()

        if buscar:
            qs = qs.filter(
                Q(cliente__nome__icontains=buscar) |
                Q(id__icontains=buscar)
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(self.request, 'Não existem empréstimos cadastrados com esse critério!')
        return context


class EmprestimoAddView(SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo adicionado com sucesso!'

    def form_valid(self, form):
        response = super().form_valid(form)
        copias_selecionadas = self.request.POST.getlist('copias')
        incluir_portao = self.request.POST.get('incluir_portao') == 'on'

        # Salvar cópias selecionadas
        for copia_id in copias_selecionadas:
            copia = CopiaChave.objects.get(id=copia_id)
            ItemEmprestimo.objects.create(
                emprestimo=self.object,
                copia_chave=copia,
                status='EMPRESTADA'
            )
            copia.status = 'EMPRESTADA'
            copia.save()

        # Se marcou para incluir portão automaticamente
        if incluir_portao and copias_selecionadas:
            copia_id = copias_selecionadas[0]  # Pega a primeira cópia selecionada
            copia = CopiaChave.objects.get(id=copia_id)
            
            # Verifica se é de Chalé Exclusivo e tem portão associado
            propriedade = copia.chave.propriedade
            if hasattr(propriedade, 'portao_associado') and propriedade.portao_associado:
                # Encontra a chave do portão
                chaves_portao = propriedade.portao_associado.chaves.all()
                if chaves_portao.exists():
                    chave_portao = chaves_portao.first()
                    # Tenta encontrar qualquer cópia da chave do portão
                    copia_portao = chave_portao.copias.first()
                    if copia_portao:
                        ItemEmprestimo.objects.create(
                            emprestimo=self.object,
                            copia_chave=copia_portao,
                            status='EMPRESTADA'
                        )
                        copia_portao.status = 'EMPRESTADA'
                        copia_portao.save()

        return response


class EmprestimoUpdateView(SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Empréstimo alterado com sucesso!'

    def form_valid(self, form):
        # Primeiro, restaura o status das cópias antigas
        for item in self.object.itens.all():
            item.copia_chave.status = 'DISPONIVEL'
            item.copia_chave.save()
        
        self.object.itens.all().delete()

        response = super().form_valid(form)
        copias_selecionadas = self.request.POST.getlist('copias')
        incluir_portao = self.request.POST.get('incluir_portao') == 'on'

        # Salvar cópias selecionadas
        for copia_id in copias_selecionadas:
            copia = CopiaChave.objects.get(id=copia_id)
            ItemEmprestimo.objects.create(
                emprestimo=self.object,
                copia_chave=copia,
                status='EMPRESTADA'
            )
            copia.status = 'EMPRESTADA'
            copia.save()

        # Se marcou para incluir portão automaticamente
        if incluir_portao and copias_selecionadas:
            copia_id = copias_selecionadas[0]  # Pega a primeira cópia selecionada
            copia = CopiaChave.objects.get(id=copia_id)
            
            # Verifica se é de Chalé Exclusivo e tem portão associado
            propriedade = copia.chave.propriedade
            if hasattr(propriedade, 'portao_associado') and propriedade.portao_associado:
                # Encontra a chave do portão
                chaves_portao = propriedade.portao_associado.chaves.all()
                if chaves_portao.exists():
                    chave_portao = chaves_portao.first()
                    # Tenta encontrar qualquer cópia da chave do portão
                    copia_portao = chave_portao.copias.first()
                    if copia_portao:
                        ItemEmprestimo.objects.create(
                            emprestimo=self.object,
                            copia_chave=copia_portao,
                            status='EMPRESTADA'
                        )
                        copia_portao.status = 'EMPRESTADA'
                        copia_portao.save()

        return response


class EmprestimoDeleteView(SuccessMessageMixin, DeleteView):
    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')

    def delete(self, request, *args, **kwargs):
        emprestimo = self.get_object()
        for item in emprestimo.itens.all():
            item.copia_chave.status = 'DISPONIVEL'
            item.copia_chave.save()

        return super().delete(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        emprestimo = self.object
        return f'Empréstimo "{emprestimo.id}" foi deletado com sucesso!'


class EmprestimoToggleStatusView(View):
    def get(self, request, pk):
        emprestimo = Emprestimo.objects.get(pk=pk)

        if emprestimo.data_devolucao is None:
            emprestimo.data_devolucao = emprestimo.data_devolucao or None
            for item in emprestimo.itens.all():
                item.copia_chave.status = 'DISPONIVEL'
                item.copia_chave.save()
                item.status = 'DEVOLVIDA'
                item.data_devolucao_item = emprestimo.data_devolucao
                item.save()
        else:
            emprestimo.data_devolucao = None
            for item in emprestimo.itens.all():
                item.copia_chave.status = 'EMPRESTADA'
                item.copia_chave.save()
                item.status = 'EMPRESTADA'
                item.data_devolucao_item = None
                item.save()

        emprestimo.save()
        messages.success(request, f'Empréstimo alterado para: {emprestimo.get_status()}')
        return HttpResponseRedirect(reverse_lazy('emprestimos'))


class EmprestimoSalvarDevolucaoView(View):
    def post(self, request, pk):
        try:
            data = json.loads(request.body)
            data_devolucao = data.get('data_devolucao')
            
            emprestimo = Emprestimo.objects.get(pk=pk)
            emprestimo.data_devolucao = data_devolucao
            emprestimo.save()
            
            # Marca todos os itens como DEVOLVIDA
            for item in emprestimo.itens.all():
                item.copia_chave.status = 'DISPONIVEL'
                item.copia_chave.save()
                item.status = 'DEVOLVIDA'
                item.data_devolucao_item = data_devolucao
                item.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})