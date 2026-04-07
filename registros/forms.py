from django import forms
from .models import Registro


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = '__all__'
        error_messages = {
            'tipo_evento': {'required': 'O tipo de evento é um campo obrigatório'},
            'copia': {'required': 'O ID da cópia é um campo obrigatório'},
            'descricao': {'required': 'A descrição é um campo obrigatório'},
        }
