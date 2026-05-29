from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Chave, CopiaChave
from .forms import ChaveModelForm, CopiaChaveModelForm


class ChavesView(PermissionRequiredMixin, ListView):
    model = Chave
    template_name = 'chaves.html'
    context_object_name = 'object_list' #pro template conseguir acessar a lista de chaves como object_list
    paginate_by = 10
    permission_required = 'chaves.view_chave'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = Chave.objects.all()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(self.request, 'Não existem chaves cadastradas com esse nome!')
        return context

class ChaveAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave adicionada com sucesso!'
    permission_required = 'chaves.add_chave'


class ChaveUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave alterada com sucesso!'
    permission_required = 'chaves.change_chave'


class ChaveDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Chave
    template_name = 'chave_apagar.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave apagada com sucesso!'
    permission_required = 'chaves.delete_chave'


class CopiasChaveView(PermissionRequiredMixin, ListView):
    model = CopiaChave
    template_name = 'copias.html'
    context_object_name = 'object_list'
    paginate_by = 10
    permission_required = 'chaves.view_copiachave'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = CopiaChave.objects.all()

        if buscar:
            qs = qs.filter(codigo__icontains=buscar)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(self.request, 'Não existem cópias cadastradas com esse código!')
        return context

class CopiaChaveAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CopiaChave
    form_class = CopiaChaveModelForm
    template_name = 'copia_form.html'
    success_url = reverse_lazy('copias')
    success_message = 'Cópia adicionada com sucesso!'
    permission_required = 'chaves.add_copiachave'


class CopiaChaveUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CopiaChave
    form_class = CopiaChaveModelForm
    template_name = 'copia_form.html'
    success_url = reverse_lazy('copias')
    success_message = 'Cópia alterada com sucesso!'
    permission_required = 'chaves.change_copiachave'

class CopiaChaveDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CopiaChave
    template_name = 'copia_apagar.html'
    success_url = reverse_lazy('copias')
    success_message = 'Cópia apagada com sucesso!'
    permission_required = 'chaves.delete_copiachave'
