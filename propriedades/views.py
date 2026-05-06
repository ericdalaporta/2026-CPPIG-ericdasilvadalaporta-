from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Propriedade, chale_comum, chale_exclusivo, Portao
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
    
    def form_valid(self, form):
        tipo = form.cleaned_data['tipo']
        nome = form.cleaned_data['nome']
        portao_associado = form.cleaned_data.get('portao_associado')
        
        if tipo == 'CHALE_COMUM':
            self.object = chale_comum(nome=nome, tipo=tipo, portao_associado=portao_associado)
        elif tipo == 'CHALE_EXCLUSIVO':
            self.object = chale_exclusivo(nome=nome, tipo=tipo, portao_associado=portao_associado)
        elif tipo == 'PORTAO':
            self.object = Portao(nome=nome, tipo=tipo, portao_associado=portao_associado)
        else:
            self.object = Propriedade(nome=nome, tipo=tipo, portao_associado=portao_associado)
        
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PropriedadeUpdateView(SuccessMessageMixin, UpdateView):
    model = Propriedade
    form_class = PropriedadeModelForm
    template_name = 'propriedade_form.html'
    success_url = reverse_lazy('propriedades')
    success_message = 'Propriedade alterada com sucesso!'


class PropriedadeDeleteView(SuccessMessageMixin, DeleteView):
    model = Propriedade
    template_name = 'propriedade_apagar.html'
    success_url = reverse_lazy('propriedades')
    success_message = 'Propriedade apagada com sucesso!'