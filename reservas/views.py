from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages

from .models import Reserva
from .forms import ReservaModelForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class ReservasView(PermissionRequiredMixin, ListView): # a reserva eh buscada apenas pelo cliente__nome__icontains
    model = Reserva
    template_name = 'reservas.html'
    context_object_name = 'object_list'
    paginate_by = 10
    permission_required = 'reservas.view_reserva'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = Reserva.objects.all()

        if buscar:
            qs = qs.filter(cliente__nome__icontains=buscar)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(
                self.request,
                'Não existem reservas cadastradas para esse cliente!'
            )

        return context

class ReservaAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva adicionada com sucesso!'
    permission_required = 'reservas.add_reserva'


class ReservaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva alterada com sucesso!'
    permission_required = 'reservas.change_reserva'


class ReservaDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Reserva
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva apagada com sucesso!'
    permission_required = 'reservas.delete_reserva'

#adicionar isso num futuro ReservaExibir

    def enviar_email(self, reserva):
        email = []
        email.append(reserva.cliente.email)
        # preciso refazer essa parte toda, não tenho nada do que tem no lavacar

