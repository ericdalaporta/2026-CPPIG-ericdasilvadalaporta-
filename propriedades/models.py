from django.db import models
from django.db.models import Q


class Propriedade(models.Model):
    TIPO_CHOICES = [
        ('CHALE_COMUM', 'Chalé Comum'),
        ('CHALE_EXCLUSIVO', 'Chalé Exclusivo'),
        ('PORTAO', 'Portão'),
    ]
    
    nome = models.CharField('Nome', max_length=70, blank=False, help_text='Nome da propriedade')
    
    tipo = models.CharField('Tipo', max_length=50, choices=TIPO_CHOICES, help_text='Tipo de propriedade')
    
    portao_associado = models.ForeignKey(
        'propriedades.Portao',
        verbose_name='Portão Associado',
        help_text='Portão associado a este chalé exclusivo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chales_exclusivos'
    )

    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'

    def __str__(self):
        return self.nome
    
    def get_tipo_display_custom(self):
        return dict(self.TIPO_CHOICES).get(self.tipo, 'Desconhecido')

    
class chale_comum(Propriedade):
    class Meta:
        verbose_name = 'Chale comum'
        verbose_name_plural = 'Chales comum'


class chale_exclusivo(Propriedade):
    class Meta:
        verbose_name = 'Chale exclusivo'
        verbose_name_plural = 'Chales exclusivos'


class Portao(Propriedade):
    
    propriedade_linkada = models.ForeignKey(
        'propriedades.Propriedade',
        verbose_name='Propriedade Linkada',
        help_text='Propriedade na qual este portão está localizado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='portoes_linkados',
        limit_choices_to=~Q(tipo='PORTAO') #o campo só mostra opcoes do tipo nao portao
    )
    
    class Meta:
        verbose_name = 'Portão'
        verbose_name_plural = 'Portões'