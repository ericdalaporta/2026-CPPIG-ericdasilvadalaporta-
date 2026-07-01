from django import forms

from .models import Cliente

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['foto', 'nome', 'telefone', 'email']

        error_messages = {
            'foto': {'invalid_image': 'Formato de imagem inválido'},
            'nome': {'required': 'O Nome do cliente é um campo obrigatório'},
            'telefone': {'required': 'O Telefone é um campo obrigatório'},
            'email': {'required': 'O Email é um campo obrigatório', 'unique': 'Email já cadastrado'},
        }