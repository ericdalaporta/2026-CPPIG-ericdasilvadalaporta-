from django import forms

from .models import Chave, CopiaChave

class ChaveModelForm(forms.ModelForm): #cria um formulario baseado no model chave
    class Meta:
        model = Chave
        fields = '__all__' #pega todo conteudo de model

        error_messages = {
            'nome': {'required': 'O Nome da chave é um campo obrigatório'},
        }


class CopiaChaveModelForm(forms.ModelForm):
    class Meta:
        model = CopiaChave
        fields = '__all__'

        error_messages = {
            'codigo': {'required': 'O Código é um campo obrigatório'},
            'status': {'required': 'O Status é um campo obrigatório'},
        }
