from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.core.paginator import Paginator
from django.contrib import messages

from .models import Chave, CopiaChave
from .forms import ChaveModelForm, CopiaChaveModelForm


class ChavesView(ListView):
    model = Chave
    template_name = 'chaves.html'
    context_object_name = 'object_list'
    paginate_by = 10

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

class ChaveAddView(SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave adicionada com sucesso!'


class ChaveUpdateView(SuccessMessageMixin, UpdateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave alterada com sucesso!'


class ChaveDeleteView(SuccessMessageMixin, DeleteView):
    model = Chave
    template_name = 'chave_apagar.html'
    success_url = reverse_lazy('chaves')
    
    def get_success_message(self, cleaned_data):
        chave = self.object
        return f'Chave "{chave.nome}" foi deletada com sucesso!'


class CopiasChaveView(ListView):
    model = CopiaChave
    template_name = 'copias.html'
    context_object_name = 'object_list'
    paginate_by = 10

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

class CopiaChaveAddView(SuccessMessageMixin, CreateView):
    model = CopiaChave
    form_class = CopiaChaveModelForm
    template_name = 'copia_form.html'
    success_url = reverse_lazy('copias')
    success_message = 'Cópia adicionada com sucesso!'


class CopiaChaveUpdateView(SuccessMessageMixin, UpdateView):
    model = CopiaChave
    form_class = CopiaChaveModelForm
    template_name = 'copia_form.html'
    success_url = reverse_lazy('copias')
    success_message = 'Cópia alterada com sucesso!'


class CopiaChaveDeleteView(SuccessMessageMixin, DeleteView):
    model = CopiaChave
    template_name = 'copia_apagar.html'
    success_url = reverse_lazy('copias')
    
    def get_success_message(self, cleaned_data):
        copia = self.object
        return f'Cópia "{copia.codigo}" foi deletada com sucesso!'
