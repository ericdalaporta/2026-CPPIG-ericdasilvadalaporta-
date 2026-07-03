from django.urls import path

from .views import (
    ReservasView,
    ReservaAddView,
    ReservaUpdateView,
    ReservaDeleteView,
    ReservaConverterEmprestimoView,
    ReservaFinalizarView,
)

urlpatterns = [
    path('reservas', ReservasView.as_view(), name='reservas'),
    path('reserva/adicionar/', ReservaAddView.as_view(), name='reserva_adicionar'),
    path('<int:pk>/reserva/editar/', ReservaUpdateView.as_view(), name='reserva_editar'),
    path('<int:pk>/reserva/apagar/', ReservaDeleteView.as_view(), name='reserva_apagar'),
    path('<int:pk>/reserva/converter-emprestimo/', ReservaConverterEmprestimoView.as_view(), name='reserva_converter_emprestimo'),
    path('<int:pk>/reserva/finalizar/', ReservaFinalizarView.as_view(), name='reserva_finalizar'),
]