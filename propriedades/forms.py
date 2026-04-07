from django import forms
from .models import Propriedade


class PropriedadeForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = '__all__'
        error_messages = {
            'nome': {'required': 'O nome da propriedade é um campo obrigatório', 'unique': 'Essa propriedade já foi cadastrada'},
            'classificacao': {'required': 'A classificação é um campo obrigatório'},
        }
