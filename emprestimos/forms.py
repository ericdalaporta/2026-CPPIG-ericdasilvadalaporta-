from django import forms
from django.db.models import Q

from .models import Emprestimo, ItemEmprestimo
from chaves.models import CopiaChave


class EmprestimoModelForm(forms.ModelForm):

    # campo extra que permite selecionar várias cópias.
    copias = forms.ModelMultipleChoiceField(
        queryset=CopiaChave.objects.filter(status='DISPONIVEL'),
        required=False,
        label='Cópias de Chave'
    )

    class Meta:
        # este form cria ou edita um Emprestimo.
        model = Emprestimo

        fields = [
            'cliente',
            'data_retirada',
            'data_prevista',
        ]

        widgets = {
            'data_retirada': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'data_prevista': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # se o empréstimo já possui ID, ele está sendo editado.
        if self.instance.pk:

            # pega os IDs das cópias que já pertencem ao empréstimo.
            copias_vinculadas = list(
                self.instance.itens.values_list(
                    'copia_chave_id',
                    flat=True
                )
            )

            # mostra as cópias disponíveis e as cópias já vinculadas.
            self.fields['copias'].queryset = CopiaChave.objects.filter(
                Q(status='DISPONIVEL')
                | Q(id__in=copias_vinculadas)
            )

            # deixa marcadas as cópias que já estão no empréstimo.
            self.fields['copias'].initial = copias_vinculadas

        else:
            # ao criar um empréstimo, mostra somente cópias disponíveis.
            self.fields['copias'].queryset = CopiaChave.objects.filter(
                status='DISPONIVEL'
            )


class ItemEmprestimoModelForm(forms.ModelForm):

    # permite editar a cópia e o status de um ItemEmprestimo.
    class Meta:
        model = ItemEmprestimo

        fields = [
            'copia_chave',
            'status',
        ]