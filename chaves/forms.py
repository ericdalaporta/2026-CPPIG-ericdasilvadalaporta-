from django import forms

from .models import Chave, CopiaChave


class ChaveModelForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = ['nome', 'propriedade']

        error_messages = {
            'nome': {'required': 'O Nome da chave é um campo obrigatório'},
            'propriedade': {'required': 'A Propriedade é um campo obrigatório'},
        }

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        propriedade = cleaned_data.get('propriedade')

        if nome and propriedade:
            repetida = Chave.objects.filter(
                nome__iexact=nome.strip(),
                propriedade=propriedade
            )

            if self.instance.pk:
                repetida = repetida.exclude(pk=self.instance.pk)

            if repetida.exists():
                self.add_error(
                    'nome',
                    'Já existe uma chave com esse nome para essa propriedade.'
                )

        return cleaned_data


class CopiaChaveModelForm(forms.ModelForm):
    class Meta:
        model = CopiaChave
        fields = ['codigo', 'chave', 'status', 'valor_restituicao', 'observacao']

        error_messages = {
            'codigo': {'required': 'O Código é um campo obrigatório'},
            'status': {'required': 'O Status é um campo obrigatório'},
            'chave': {'required': 'A Chave é um campo obrigatório'},
        }

    def clean(self):
        cleaned_data = super().clean()
        codigo = cleaned_data.get('codigo')
        chave = cleaned_data.get('chave')
        status = cleaned_data.get('status')

        # Só bloqueia duplicidade ao cadastrar uma cópia nova. O banco do projeto já tinha
        # cópias antigas repetidas, então não forço isso em edição para não quebrar os dados existentes.
        if not self.instance.pk and codigo is not None and chave:
            if CopiaChave.objects.filter(codigo=codigo, chave=chave).exists():
                self.add_error(
                    'codigo',
                    'Já existe uma cópia com esse código para essa chave.'
                )

        if self.instance.pk and status == CopiaChave.STATUS_DISPONIVEL:
            existe_emprestimo_ativo = self.instance.itens_emprestimo.filter(
                status='EMPRESTADA',
                emprestimo__ativo=True
            ).exists()

            if existe_emprestimo_ativo:
                self.add_error(
                    'status',
                    'Esta cópia está em empréstimo ativo. Conclua ou cancele o empréstimo antes de deixá-la disponível.'
                )

        return cleaned_data
