from django import forms
from .models import Propriedade


class PropriedadeModelForm(forms.ModelForm):

    class Meta:
        model = Propriedade
        fields = ['nome', 'tipo', 'portao_associado']

        error_messages = {
            'nome': {
                'required': 'O Nome da propriedade é obrigatório'
            },
            'tipo': {
                'required': 'O Tipo é obrigatório'
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        portao_associado = cleaned_data.get('portao_associado')

        if tipo != Propriedade.TIPO_CHALE_EXCLUSIVO:
            cleaned_data['portao_associado'] = None

        if tipo == Propriedade.TIPO_CHALE_EXCLUSIVO and portao_associado:
            if portao_associado.tipo != Propriedade.TIPO_PORTAO:
                self.add_error(
                    'portao_associado',
                    'O portão associado precisa ser uma propriedade do tipo Portão.'
                )

            if self.instance.pk and portao_associado.pk == self.instance.pk:
                self.add_error(
                    'portao_associado',
                    'A propriedade não pode ser associada a ela mesma.'
                )

        return cleaned_data
