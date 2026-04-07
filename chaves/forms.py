from django import forms
from .models import Chave


class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = '__all__'
        error_messages = {
            'nome': {'required': 'O nome da chave é um campo obrigatório'},
            'id_fisico': {'required': 'O ID físico é um campo obrigatório', 'unique': 'Esse ID físico já foi cadastrado'},
            'status': {'required': 'O status é um campo obrigatório'},
            'propriedade': {'required': 'A propriedade é um campo obrigatório'},
        }
