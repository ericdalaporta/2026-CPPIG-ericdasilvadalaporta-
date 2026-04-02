from django.contrib import admin
from .models import Emprestimo


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'data_retirada', 'status', 'criado_em')
    list_filter = ('status', 'data_retirada', 'criado_em')
    search_fields = ('solicitante',)
    ordering = ('-data_retirada',)
