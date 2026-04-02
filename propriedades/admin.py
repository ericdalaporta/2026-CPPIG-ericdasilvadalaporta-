from django.contrib import admin
from .models import Propriedade


@admin.register(Propriedade)
class PropriedadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'classificacao', 'criado_em')
    list_filter = ('classificacao', 'criado_em')
    search_fields = ('nome',)
    ordering = ('-criado_em',)
