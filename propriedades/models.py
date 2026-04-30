from django.db import models


class Propriedade(models.Model):
    TIPO_CHOICES = [
        ('propriedade', 'Propriedade'),
        ('chale_comum', 'Chale Comum'),
        ('chale_exclusivo', 'Chale Exclusivo'),
    ]
    
    CLASSIFICACAO_CHOICES = [
        (True, 'Ocupada'),
        (False, 'Livre'),
    ]
    
    nome = models.CharField('Nome', max_length=70, blank=False, help_text='Nome da propriedade')
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='propriedade', blank=False)
    classificacao = models.BooleanField('Classificação', default=False, help_text='Classificação da propriedade')

    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'

    def __str__(self):
        return self.nome
    
    def get_status(self):
        return 'Ocupada' if self.classificacao else 'Livre'
    
    def toggle_status(self):
        self.classificacao = not self.classificacao
        self.save()
    
    def get_tipo_display_custom(self):
        """Retorna o tipo formatado da propriedade"""
        return self.get_tipo_display()
