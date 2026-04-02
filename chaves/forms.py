from django import forms
from .models import Chave


class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = ['nome', 'id_fisico', 'status', 'propriedade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Chave mestra prédio Y'}),
            'id_fisico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CP-001'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'propriedade': forms.Select(attrs={'class': 'form-select'}),
        }
