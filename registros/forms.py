from django import forms
from .models import Registro


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = '__all__'
        widgets = {
            'tipo_evento': forms.Select(attrs={'class': 'form-select'}),
            'copia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID da cópia'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva o evento...'}),
        }
        error_messages = {
            'tipo_evento': {'required': 'O tipo de evento é um campo obrigatório'},
            'copia': {'required': 'O ID da cópia é um campo obrigatório'},
            'descricao': {'required': 'A descrição é um campo obrigatório'},
        }
