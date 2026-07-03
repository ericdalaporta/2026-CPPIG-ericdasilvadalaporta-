from django.core.exceptions import ValidationError
from django.db import models


class Propriedade(models.Model):
    TIPO_CHALE_COMUM = 'CHALE_COMUM'
    TIPO_CHALE_EXCLUSIVO = 'CHALE_EXCLUSIVO'
    TIPO_PORTAO = 'PORTAO'

    TIPO_CHOICES = [
        (TIPO_CHALE_COMUM, 'Chalé Comum'),
        (TIPO_CHALE_EXCLUSIVO, 'Chalé Exclusivo'),
        (TIPO_PORTAO, 'Portão'),
    ]

    nome = models.CharField(
        'Nome',
        max_length=70,
        blank=False,
        help_text='Nome da propriedade'
    )

    tipo = models.CharField(
        'Tipo',
        max_length=50,
        choices=TIPO_CHOICES,
        help_text='Tipo de propriedade'
    )

    portao_associado = models.ForeignKey(
        'propriedades.Propriedade',
        verbose_name='Portão Associado',
        help_text='Portão associado a este chalé exclusivo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chales_exclusivos',
        limit_choices_to={'tipo': TIPO_PORTAO}
    )

    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def eh_portao(self):
        return self.tipo == self.TIPO_PORTAO

    @property
    def eh_chale_exclusivo(self):
        return self.tipo == self.TIPO_CHALE_EXCLUSIVO

    def clean(self):
        super().clean()

        # Só chalé exclusivo pode ter portão associado.
        if self.tipo != self.TIPO_CHALE_EXCLUSIVO and self.portao_associado_id:
            raise ValidationError({
                'portao_associado': 'Somente chalé exclusivo pode ter portão associado.'
            })

        # Um chalé não pode apontar para ele mesmo como portão.
        if self.pk and self.portao_associado_id == self.pk:
            raise ValidationError({
                'portao_associado': 'Uma propriedade não pode ser o próprio portão associado.'
            })

        # Se houver portão associado, ele precisa ser realmente do tipo PORTÃO.
        if self.portao_associado and self.portao_associado.tipo != self.TIPO_PORTAO:
            raise ValidationError({
                'portao_associado': 'A propriedade associada precisa ser do tipo Portão.'
            })

    def save(self, *args, **kwargs):
        # Evita guardar portão associado em propriedade que não é chalé exclusivo.
        if self.tipo != self.TIPO_CHALE_EXCLUSIVO:
            self.portao_associado = None

        self.full_clean()
        return super().save(*args, **kwargs)


# Mantive as classes abaixo para não quebrar migrations antigas do teu projeto.
# A lógica real usa o campo "tipo" da classe Propriedade.
class chale_comum(Propriedade):
    class Meta:
        verbose_name = 'Chale comum'
        verbose_name_plural = 'Chales comum'


class chale_exclusivo(Propriedade):
    class Meta:
        verbose_name = 'Chale exclusivo'
        verbose_name_plural = 'Chales exclusivos'


class Portao(Propriedade):
    class Meta:
        verbose_name = 'Portão'
        verbose_name_plural = 'Portões'
