from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect

from .models import Propriedade
from .forms import PropriedadeModelForm


class PropriedadesView(PermissionRequiredMixin, ListView):
    model = Propriedade
    template_name = 'propriedades.html'
    paginate_by = 10
    permission_required = 'propriedades.view_propriedade'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')

        if buscar:
            return Propriedade.objects.filter(
                nome__icontains=buscar
            )

        # Se não tiver busca, pega todas as propriedades.
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(
                self.request,
                'Não existem propriedades cadastradas com esse nome!'
            )

        return context


class PropriedadeAddView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    
    model = Propriedade
    form_class = PropriedadeModelForm
    template_name = 'propriedade_form.html'
    success_url = reverse_lazy('propriedades')
    success_message = 'Propriedade adicionada com sucesso!'
    permission_required = 'propriedades.add_propriedade'


class PropriedadeUpdateView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Propriedade
    form_class = PropriedadeModelForm
    template_name = 'propriedade_form.html'
    success_url = reverse_lazy('propriedades')
    success_message = 'Propriedade alterada com sucesso!'
    permission_required = 'propriedades.change_propriedade'


class PropriedadeDeleteView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Propriedade
    template_name = 'propriedade_apagar.html'
    success_url = reverse_lazy('propriedades')
    success_message = 'Propriedade apagada com sucesso!'
    permission_required = 'propriedades.delete_propriedade'

    def post(self, request, *args, **kwargs):
        try:
            # Tenta apagar a propriedade normalmente.
            return super().post(request, *args, **kwargs)

        except ProtectedError:
            # Aparece se existirem chaves ligadas à propriedade.
            messages.error(
                request,
                'Não é possível apagar esta propriedade porque existem chaves vinculadas a ela.'
            )

            return redirect('propriedades')