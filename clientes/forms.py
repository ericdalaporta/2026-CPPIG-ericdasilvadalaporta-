from django import forms

from .models import Cliente

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
        }

        error_messages = {
            'nome': {'required': 'O Nome do cliente é um campo obrigatório'},
            'telefone': {'required': 'O Telefone é um campo obrigatório'},
            'email': {'required': 'O Email é um campo obrigatório', 'unique': 'Email já cadastrado'},
        }