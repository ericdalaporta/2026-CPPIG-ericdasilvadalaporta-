from django import forms
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError

from .models import Emprestimo, ItemEmprestimo
from chaves.models import CopiaChave

class EmprestimoModelForm(forms.ModelForm):
    copias = forms.ModelMultipleChoiceField(
        queryset=CopiaChave.objects.filter(status='DISPONIVEL'),
        widget=forms.SelectMultiple,
        required=False,
        label='Cópias de Chave'
    )
    
    class Meta:
        model = Emprestimo
        fields = ['cliente', 'data_retirada', 'data_prevista']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['copias'].queryset = CopiaChave.objects.filter(status='DISPONIVEL')
    
    def clean(self):
        cleaned_data = super().clean()
        copias_selecionadas = self.data.getlist('copias')
        
        if not copias_selecionadas:
            raise ValidationError('Selecione pelo menos uma cópia de chave.')
        
        return cleaned_data


class ItemEmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = ItemEmprestimo
        fields = ['copia_chave', 'status']
