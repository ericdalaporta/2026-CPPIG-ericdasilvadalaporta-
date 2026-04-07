from django import forms
from .models import Emprestimo


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        error_messages = {
            'solicitante': {'required': 'O nome do solicitante é um campo obrigatório'},
            'chaves': {'required': 'Selecione pelo menos uma chave'},
            'data_devolucao_prevista': {'required': 'A data de devolução prevista é um campo obrigatório'},
        }
