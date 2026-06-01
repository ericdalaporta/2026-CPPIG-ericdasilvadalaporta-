from django import forms

from .models import Reserva

class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'chaves', 'data_inicio', 'data_fim', 'status']
        widgets = {
            'chaves': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'chaves': {'required': 'Selecione pelo menos uma chave'},
            'data_inicio': {'required': 'A Data de Início é um campo obrigatório'},
            'data_fim': {'required': 'A Data de Fim é um campo obrigatório'},
            'status': {'required': 'O Status é um campo obrigatório'},
        }
