from django.contrib import admin
from .models import Registro


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('tipo_evento', 'copia', 'data_evento')
    list_filter = ('tipo_evento', 'data_evento')
    search_fields = ('copia', 'descricao')
    ordering = ('-data_evento',)
    readonly_fields = ('data_evento',)
