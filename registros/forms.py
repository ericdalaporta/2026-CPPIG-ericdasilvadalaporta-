from django import forms
from .models import Registro


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['tipo_evento', 'copia', 'descricao']
        widgets = {
            'tipo_evento': forms.Select(attrs={'class': 'form-select'}),
            'copia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID da cópia'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
