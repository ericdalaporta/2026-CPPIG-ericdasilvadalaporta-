from django import forms

from .models import Reserva

class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'data_inicio', 'data_fim', 'status']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'data_inicio': {'required': 'A Data de Início é um campo obrigatório'},
            'data_fim': {'required': 'A Data de Fim é um campo obrigatório'},
            'status': {'required': 'O Status é um campo obrigatório'},
        }
