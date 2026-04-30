from django import forms
from django.forms.widgets import DateInput

from .models import Emprestimo

class EmprestimoModelForm(forms.ModelForm):
    data_retirada = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': False}),
        error_messages={'required': 'A Data de Retirada é um campo obrigatório'}
    )
    data_prevista = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': False}),
        error_messages={'required': 'A Data Prevista é um campo obrigatório'}
    )

    class Meta:
        model = Emprestimo
        fields = ['data_retirada', 'data_prevista']
