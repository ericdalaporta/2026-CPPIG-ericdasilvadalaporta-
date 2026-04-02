from django.urls import path
from .views import ListaReservas, CriarReserva, EditarReserva, DeletarReserva

app_name = 'reservas'

urlpatterns = [
    path('', ListaReservas.as_view(), name='list'),
    path('criar/', CriarReserva.as_view(), name='create'),
    path('<int:pk>/editar/', EditarReserva.as_view(), name='update'),
    path('<int:pk>/deletar/', DeletarReserva.as_view(), name='delete'),
]
