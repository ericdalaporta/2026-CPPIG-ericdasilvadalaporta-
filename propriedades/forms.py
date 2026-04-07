from django import forms
from .models import Propriedade


class PropriedadeForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Chalé Araucária 01'}),
            'classificacao': forms.Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'nome': {'required': 'O nome da propriedade é um campo obrigatório', 'unique': 'Essa propriedade já foi cadastrada'},
            'classificacao': {'required': 'A classificação é um campo obrigatório'},
        }
