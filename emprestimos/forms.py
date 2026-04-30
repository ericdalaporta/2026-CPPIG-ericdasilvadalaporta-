from django import forms
from django.forms.widgets import DateInput

from .models import Emprestimo

class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['data_retirada', 'data_prevista']
        widgets = {
            'data_retirada': DateInput(attrs={'type': 'date'}),
            'data_prevista': DateInput(attrs={'type': 'date'}),
        }

        error_messages = {
            'data_retirada': {'required': 'A Data de Retirada é um campo obrigatório'},
            'data_prevista': {'required': 'A Data Prevista é um campo obrigatório'},
        }
