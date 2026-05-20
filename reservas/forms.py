from django import forms
from django.core.exceptions import ValidationError

from .models import Reserva
from chaves.models import CopiaChave

class ReservaModelForm(forms.ModelForm):
    copias = forms.ModelMultipleChoiceField(
        queryset=CopiaChave.objects.filter(status='DISPONIVEL'),
        required=False,
        label='Cópias de Chave'
    )
    
    class Meta:
        model = Reserva
        fields = '__all__'
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
            # Edição: mostrar todas as cópias
            self.fields['copias'].queryset = CopiaChave.objects.all()
            # Pré-selecionar as cópias já vinculadas
            cópias_vinculadas = self.instance.copias.values_list('id', flat=True)
            self.fields['copias'].initial = cópias_vinculadas
        else:
            # Novo: mostrar só disponível
            self.fields['copias'].queryset = CopiaChave.objects.filter(status='DISPONIVEL')
    
    def clean(self):
        cleaned_data = super().clean()
        copias_selecionadas = self.data.getlist('copias')
        
        if not copias_selecionadas:
            raise ValidationError('Selecione pelo menos uma cópia de chave.')
        
        return cleaned_data
