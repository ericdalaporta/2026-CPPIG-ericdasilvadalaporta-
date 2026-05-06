from django.contrib import admin
from .models import Emprestimo, ItemEmprestimo


class ItemEmprestimoInline(admin.TabularInline):
    model = ItemEmprestimo
    extra = 0


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_retirada', 'data_prevista', 'get_status')
    inlines = [ItemEmprestimoInline]


@admin.register(ItemEmprestimo)
class ItemEmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'emprestimo', 'copia_chave', 'status', 'multa')
