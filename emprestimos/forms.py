from django import forms
from django.db.models import Q

from .models import Emprestimo, ItemEmprestimo
from chaves.models import CopiaChave


class EmprestimoModelForm(forms.ModelForm):
    copias = forms.ModelMultipleChoiceField(
        queryset=CopiaChave.objects.none(),
        required=False,
        label='Cópias de Chave'
    )

    class Meta:
        model = Emprestimo
        fields = [
            'cliente',
            'data_retirada',
            'data_prevista',
            'valor_multa_por_hora',
            'tolerancia_minutos',
        ]

        widgets = {
            'data_retirada': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'data_prevista': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cliente'].required = True

        self.fields['data_retirada'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['data_prevista'].input_formats = ['%Y-%m-%dT%H:%M']

        status_disponivel = getattr(CopiaChave, 'STATUS_DISPONIVEL', 'DISPONIVEL')

        if self.instance.pk:
            copias_vinculadas = list(
                self.instance.itens.values_list('copia_chave_id', flat=True)
            )

            self.fields['copias'].queryset = CopiaChave.objects.filter(
                Q(status=status_disponivel)
                | Q(id__in=copias_vinculadas)
            ).select_related('chave__propriedade__portao_associado')

            self.fields['copias'].initial = copias_vinculadas

        else:
            self.fields['copias'].queryset = CopiaChave.objects.filter(
                status=status_disponivel
            ).select_related('chave__propriedade__portao_associado')

    def clean(self):
        cleaned_data = super().clean()

        cliente = cleaned_data.get('cliente')
        data_retirada = cleaned_data.get('data_retirada')
        data_prevista = cleaned_data.get('data_prevista')
        valor_multa_por_hora = cleaned_data.get('valor_multa_por_hora')
        tolerancia_minutos = cleaned_data.get('tolerancia_minutos')

        if not cliente:
            self.add_error('cliente', 'Selecione o cliente do empréstimo.')

        if data_retirada and data_prevista and data_retirada >= data_prevista:
            self.add_error(
                'data_prevista',
                'A data e hora prevista precisa ser posterior à data e hora de retirada.'
            )

        if valor_multa_por_hora is not None and valor_multa_por_hora < 0:
            self.add_error(
                'valor_multa_por_hora',
                'O valor da multa por hora não pode ser negativo.'
            )

        if tolerancia_minutos is not None and tolerancia_minutos > 1440:
            self.add_error(
                'tolerancia_minutos',
                'A tolerância não pode ser maior que 24 horas.'
            )

        return cleaned_data


class ItemEmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = ItemEmprestimo
        fields = [
            'copia_chave',
            'status',
            'observacao',
        ]