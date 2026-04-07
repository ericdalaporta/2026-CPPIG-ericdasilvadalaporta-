from django import forms
from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do solicitante'}),
            'chaves': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'data_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'data_fim': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        error_messages = {
            'solicitante': {'required': 'O nome do solicitante é um campo obrigatório'},
            'chaves': {'required': 'Selecione pelo menos uma chave'},
            'data_inicio': {'required': 'A data de início é um campo obrigatório'},
            'data_fim': {'required': 'A data de término é um campo obrigatório'},
        }
