from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Propriedade
from .forms import PropriedadeModelForm


class PropriedadesView(ListView):
    model = Propriedade
    template_name = 'propriedades.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = Propriedade.objects.all()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(self.request, 'Não existem propriedades cadastradas com esse nome!')
        return context

class PropriedadeAddView(SuccessMessageMixin, CreateView):
    model = Propriedade
    form_class = PropriedadeModelForm
    template_name = 'propriedade_form.html'
    success_url = reverse_lazy('propriedades')
    success_message = 'Propriedade adicionada com sucesso!'


class PropriedadeUpdateView(SuccessMessageMixin, UpdateView):
    model = Propriedade
    form_class = PropriedadeModelForm
    template_name = 'propriedade_form.html'
    success_url = reverse_lazy('propriedades')
    success_message = 'Propriedade alterada com sucesso!'


class PropriedadeDeleteView(DeleteView):
    model = Propriedade
    template_name = 'propriedade_apagar.html'
    success_url = reverse_lazy('propriedades')


class PropriedadeToggleStatusView(View):
    def get(self, request, pk):
        propriedade = Propriedade.objects.get(pk=pk)
        propriedade.toggle_status()
        messages.success(request, f'Propriedade alterada para: {propriedade.get_status()}')
        return HttpResponseRedirect(reverse_lazy('propriedades'))
