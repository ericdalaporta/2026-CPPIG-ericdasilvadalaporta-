from django import forms
from .models import Propriedade


class PropriedadeForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = ['nome', 'classificacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Chalé Araucária 01'}),
            'classificacao': forms.Select(attrs={'class': 'form-select'}),
        }
