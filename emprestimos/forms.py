from django import forms
from django.forms.widgets import DateInput

from .models import Emprestimo

class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['cliente', 'propriedade', 'copia', 'data_retirada', 'data_prevista']
