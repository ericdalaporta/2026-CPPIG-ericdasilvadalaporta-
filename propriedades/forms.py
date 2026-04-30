from django import forms

from .models import Propriedade

class PropriedadeModelForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = ['nome', 'numero']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
        }

        error_messages = {
            'nome': {'required': 'O Nome da propriedade é um campo obrigatório'},
            'numero': {'required': 'O número da propriedade é um campo obrigatório'},
        }


