from django import forms

from .models import Propriedade

class PropriedadeModelForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = ['nome']

        error_messages = {
            'nome': {'required': 'O Nome da propriedade é um campo obrigatório'},
        }
