from django import forms

from .models import Propriedade

class PropriedadeModelForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }

        error_messages = {
            'nome': {'required': 'O Nome da propriedade é um campo obrigatório'},
            'tipo': {'required': 'O Tipo da propriedade é um campo obrigatório'},
        }


