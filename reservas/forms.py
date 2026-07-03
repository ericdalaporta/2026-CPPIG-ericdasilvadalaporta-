from django import forms

from .models import Reserva
from .services import (
    buscar_conflitos_emprestimo,
    buscar_conflitos_reserva,
)


class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'cliente',
            'chaves',
            'data_inicio',
            'data_fim',
            'status',
            'observacao',
        ]

        widgets = {
            'chaves': forms.CheckboxSelectMultiple(),
            'data_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'data_fim': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }

        error_messages = {
            'chaves': {'required': 'Selecione pelo menos uma chave.'},
            'data_inicio': {'required': 'A data e hora de início são obrigatórias.'},
            'data_fim': {'required': 'A data e hora de fim são obrigatórias.'},
            'status': {'required': 'O status é obrigatório.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cliente'].required = True
        self.fields['chaves'].required = True
        self.fields['status'].choices = Reserva.STATUS_CHOICES

        self.fields['data_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['data_fim'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean(self):
        cleaned_data = super().clean()

        cliente = cleaned_data.get('cliente')
        chaves = cleaned_data.get('chaves')
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        status = cleaned_data.get('status')

        if not cliente:
            self.add_error('cliente', 'Selecione o cliente da reserva.')

        if data_inicio and data_fim and data_inicio >= data_fim:
            self.add_error(
                'data_fim',
                'A data e hora final precisa ser posterior à data e hora inicial.'
            )

        if not chaves:
            self.add_error('chaves', 'Selecione pelo menos uma chave.')

        if not chaves or not data_inicio or not data_fim:
            return cleaned_data

        if status in [
            Reserva.STATUS_CANCELADA,
            Reserva.STATUS_FINALIZADA,
            Reserva.STATUS_CONVERTIDA,
        ]:
            return cleaned_data

        conflitos_reserva = buscar_conflitos_reserva(
            chaves,
            data_inicio,
            data_fim,
            reserva_id=self.instance.pk if self.instance.pk else None
        )

        if conflitos_reserva.exists():
            reservas = ', '.join(str(reserva.id) for reserva in conflitos_reserva[:5])

            self.add_error(
                'chaves',
                f'Existe conflito com outra reserva ativa nesse período. Reserva(s): {reservas}.'
            )

            return cleaned_data

        conflitos_emprestimo = buscar_conflitos_emprestimo(
            chaves,
            data_inicio,
            data_fim
        )

        if conflitos_emprestimo.exists():
            emprestimos = ', '.join(str(emprestimo.id) for emprestimo in conflitos_emprestimo[:5])

            self.add_error(
                'chaves',
                f'Existe chave emprestada nesse período. Empréstimo(s): {emprestimos}.'
            )

            return cleaned_data

        return cleaned_data