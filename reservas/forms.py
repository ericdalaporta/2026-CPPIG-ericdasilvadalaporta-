from django import forms
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError

from .models import Reserva
from chaves.models import CopiaChave

class ReservaModelForm(forms.ModelForm):
    copias = forms.ModelMultipleChoiceField(
        queryset=CopiaChave.objects.filter(status='DISPONIVEL'),
        widget=forms.SelectMultiple,
        required=False,
        label='Cópias de Chave'
    )
    
    class Meta:
        model = Reserva
        fields = ['cliente', 'data_inicio', 'data_fim', 'status']

        error_messages = {
            'data_inicio': {'required': 'A Data de Início é um campo obrigatório'},
            'data_fim': {'required': 'A Data de Fim é um campo obrigatório'},
            'status': {'required': 'O Status é um campo obrigatório'},
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['copias'].queryset = CopiaChave.objects.filter(status='DISPONIVEL')
        # se to editando, mostrar as cópias já selecionadas
        if self.instance.pk:
            self.fields['copias'].initial = self.instance.copias.all()
    
    def clean(self):
        cleaned_data = super().clean()
        copias_selecionadas = self.data.getlist('copias')
        
        if not copias_selecionadas:
            raise ValidationError('Selecione pelo menos uma cópia de chave.')
        
        return cleaned_data
