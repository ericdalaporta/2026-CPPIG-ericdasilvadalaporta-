from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Reserva
from .forms import ReservaForm


class ListaReservas(ListView):
    model = Reserva
    template_name = 'reservas.html'
    context_object_name = 'reservas'
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['pagina'] = 'reservas'
        return contexto


class CriarReserva(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas:list')


class EditarReserva(UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas:list')


class DeletarReserva(DeleteView):
    model = Reserva
    template_name = 'reserva_confirm_delete.html'
    success_url = reverse_lazy('reservas:list')
