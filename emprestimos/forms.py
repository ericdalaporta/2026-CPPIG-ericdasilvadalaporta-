from django import forms
from django.core.exceptions import ValidationError

from .models import Emprestimo, ItemEmprestimo
from chaves.models import CopiaChave

class EmprestimoModelForm(forms.ModelForm):
    copias = forms.ModelMultipleChoiceField(
        queryset=CopiaChave.objects.filter(status='DISPONIVEL'),
        required=False,
        label='Cópias de Chave'
    )
    
    class Meta:
        model = Emprestimo
        fields = '__all__'
        widgets = {
            'data_retirada': forms.DateInput(attrs={'type': 'date'}),
            'data_prevista': forms.DateInput(attrs={'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se está editando (já tem ID), mostrar TODAS as cópias
        # Se for novo, mostrar só DISPONIVEL
        if self.instance.pk:
            # Edição: mostrar todas as cópias
            self.fields['copias'].queryset = CopiaChave.objects.all()
            # Pré-selecionar as cópias já vinculadas
            cópias_vinculadas = self.instance.itens.values_list('copia_chave_id', flat=True)
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


class ItemEmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = ItemEmprestimo
        fields = ['copia_chave', 'status']
