from django import forms
from .models import Emprestimo


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['solicitante', 'chaves', 'data_devolucao_prevista']
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'chaves': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'data_devolucao_prevista': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
