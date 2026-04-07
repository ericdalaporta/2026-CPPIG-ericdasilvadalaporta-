from django import forms
from .models import Chave


class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Chave mestra prédio Y'}),
            'id_fisico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CP-001'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'propriedade': forms.Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'nome': {'required': 'O nome da chave é um campo obrigatório'},
            'id_fisico': {'required': 'O ID físico é um campo obrigatório', 'unique': 'Esse ID físico já foi cadastrado'},
            'status': {'required': 'O status é um campo obrigatório'},
            'propriedade': {'required': 'A propriedade é um campo obrigatório'},
        }
