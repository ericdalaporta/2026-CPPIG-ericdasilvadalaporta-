from django.contrib import admin
from .models import Chave


@admin.register(Chave)
class ChaveAdmin(admin.ModelAdmin):
    list_display = ('nome', 'id_fisico', 'status', 'propriedade', 'criado_em',)
    list_filter = ('status', 'criado_em')
    search_fields = ('nome', 'id_fisico')
    ordering = ('-criado_em',)
