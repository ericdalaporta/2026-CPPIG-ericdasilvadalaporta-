from django import forms
from django.forms.widgets import DateInput

from .models import Reserva

class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'propriedade', 'data_inicio', 'data_fim', 'status']

        error_messages = {
            'data_inicio': {'required': 'A Data de Início é um campo obrigatório'},
            'data_fim': {'required': 'A Data de Fim é um campo obrigatório'},
            'status': {'required': 'O Status é um campo obrigatório'},
        }
