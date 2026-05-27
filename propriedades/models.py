from django.db import models

class Propriedade(models.Model):
    TIPO_CHOICES = [
        ('CHALE_COMUM', 'Chalé Comum'),
        ('CHALE_EXCLUSIVO', 'Chalé Exclusivo'),
        ('PORTAO', 'Portão'),
    ]
    
    nome = models.CharField('Nome', max_length=70, blank=False, help_text='Nome da propriedade')
    
    tipo = models.CharField('Tipo', max_length=50, choices=TIPO_CHOICES, help_text='Tipo de propriedade') 
    
    portao_associado = models.ForeignKey( 
        'propriedades.Propriedade',
        verbose_name='Portão Associado',
        help_text='Portão associado a este chalé exclusivo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chales_exclusivos',
        limit_choices_to={'tipo': 'PORTAO'}
    )

    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'

    def __str__(self):
        return self.nome
    
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