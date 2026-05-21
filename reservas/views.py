from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages

from .models import Reserva
from .forms import ReservaModelForm


class ReservasView(ListView):
    model = Reserva
    template_name = 'reservas.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = Reserva.objects.all()

        if buscar:
            qs = qs.filter(
                Q(cliente__nome__icontains=buscar) |
                Q(propriedade__nome__icontains=buscar) |
                Q(id__icontains=buscar)
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(self.request, 'Não existem reservas cadastradas com esse critério!')
        return context


class ReservaAddView(SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva adicionada com sucesso!'


class ReservaUpdateView(SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva alterada com sucesso!'

    def form_valid(self, form):
        response = super().form_valid(form)
        copias_selecionadas = self.request.POST.getlist('copias')
        self.object.copias.set(copias_selecionadas)
        return response


class ReservaDeleteView(SuccessMessageMixin, DeleteView):
    model = Reserva
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva apagada com sucesso!'

#adicionar isso num futuro ReservaExibir

    def enviar_email(self, reserva):
        email = []
        email.append(reserva.cliente.email)
        # preciso refazer essa parte toda, não tenho nada do que tem no lavacar
