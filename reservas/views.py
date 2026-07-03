from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ReservaModelForm
from .models import Reserva
from .services import (
    RegraReservaError,
    cancelar_reserva,
    converter_reserva_em_emprestimo,
    finalizar_reserva,
)


class ReservasView(PermissionRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas.html'
    context_object_name = 'object_list'
    paginate_by = 10
    permission_required = 'reservas.view_reserva'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')

        qs = Reserva.objects.select_related(
            'cliente',
            'emprestimo_gerado'
        ).prefetch_related('chaves').order_by('-data_inicio', '-id')

        if buscar:
            qs = qs.filter(
                Q(id__icontains=buscar)
                | Q(cliente__nome__icontains=buscar)
                | Q(chaves__nome__icontains=buscar)
            ).distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not context['object_list'] and self.request.GET.get('buscar'):
            messages.info(
                self.request,
                'Não existem reservas cadastradas para essa busca!'
            )

        return context


class ReservaAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva adicionada com sucesso!'
    permission_required = 'reservas.add_reserva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chaves_selecionadas'] = []
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['chaves_selecionadas'] = self.request.POST.getlist('chaves')
        return self.render_to_response(context)


class ReservaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva alterada com sucesso!'
    permission_required = 'reservas.change_reserva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            context['chaves_selecionadas'] = self.request.POST.getlist('chaves')
        else:
            context['chaves_selecionadas'] = [
                str(chave_id)
                for chave_id in self.object.chaves.values_list('id', flat=True)
            ]

        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['chaves_selecionadas'] = self.request.POST.getlist('chaves')
        return self.render_to_response(context)


class ReservaDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Reserva
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva cancelada com sucesso! O histórico foi preservado.'
    permission_required = 'reservas.delete_reserva'

    def form_valid(self, form):
        try:
            cancelar_reserva(self.object)
            messages.success(self.request, self.success_message)
        except (RegraReservaError, ValidationError) as erro:
            mensagens = getattr(erro, 'messages', [str(erro)])

            for mensagem in mensagens:
                messages.error(self.request, mensagem)

        return redirect(self.success_url)


class ReservaConverterEmprestimoView(PermissionRequiredMixin, View):
    permission_required = 'emprestimos.add_emprestimo'

    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)

        try:
            emprestimo = converter_reserva_em_emprestimo(reserva)
            messages.success(
                request,
                f'Reserva convertida em empréstimo #{emprestimo.id} com sucesso!'
            )
        except (RegraReservaError, ValidationError) as erro:
            mensagens = getattr(erro, 'messages', [str(erro)])

            for mensagem in mensagens:
                messages.error(request, mensagem)

        return redirect('reservas')


class ReservaFinalizarView(PermissionRequiredMixin, View):
    permission_required = 'reservas.change_reserva'

    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)

        try:
            finalizar_reserva(reserva)
            messages.success(request, 'Reserva finalizada com sucesso!')
        except (RegraReservaError, ValidationError) as erro:
            mensagens = getattr(erro, 'messages', [str(erro)])

            for mensagem in mensagens:
                messages.error(request, mensagem)

        return redirect('reservas')