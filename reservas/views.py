from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.core.paginator import Paginator
from django.contrib import messages

from .models import Reserva
from .forms import ReservaModelForm


class ReservasView(ListView):
    model = Reserva
    template_name = 'reservas.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        qs = Reserva.objects.all()
        return qs

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


class ReservaDeleteView(SuccessMessageMixin, DeleteView):
    model = Reserva
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    
    def get_success_message(self, cleaned_data):
        reserva = self.object
        return f'Reserva "{reserva.id}" foi deletada com sucesso!'
