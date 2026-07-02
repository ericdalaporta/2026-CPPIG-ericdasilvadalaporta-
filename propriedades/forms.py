from django import forms
from .models import Propriedade


class PropriedadeModelForm(forms.ModelForm):

    class Meta:
        model = Propriedade

        fields = '__all__' # pega todos os campos de models e faz o form automaticamente

        error_messages = {
            
            'nome': {
                'required': 'O Nome da propriedade é obrigatório'
            },
            'tipo': {
                'required': 'O Tipo é obrigatório'
            },
        }