from django import forms

from .models import Cliente

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

        error_messages = {
            'nome': {'required': 'O Nome do cliente é um campo obrigatório'},
            'telefone': {'required': 'O Telefone é um campo obrigatório'},
            'email': {'required': 'O Email é um campo obrigatório', 'unique': 'Email já cadastrado'},
        }