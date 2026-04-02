from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'data_inicio', 'status', 'criado_em')
    list_filter = ('status', 'data_inicio', 'criado_em')
    search_fields = ('solicitante',)
    ordering = ('-data_inicio',)
