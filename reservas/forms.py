from django import forms
from django.forms.widgets import DateInput

from .models import Reserva

class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'data_inicio': DateInput(attrs={'type': 'date'}),
            'data_fim': DateInput(attrs={'type': 'date'}),
        }

        error_messages = {
            'data_inicio': {'required': 'A Data de Início é um campo obrigatório'},
            'data_fim': {'required': 'A Data de Fim é um campo obrigatório'},
            'status': {'required': 'O Status é um campo obrigatório'},
        }
