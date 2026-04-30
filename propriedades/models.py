from django.db import models


class Propriedade(models.Model):

    CLASSIFICACAO_CHOICES = [
        (True, 'Ocupada'),
        (False, 'Livre'),
    ]
    
    nome = models.CharField('Nome', max_length=70, blank=False, help_text='Nome da propriedade')
    numero = models.CharField('Número', max_length=50, blank=False, help_text='Número da propriedade')
    classificacao = models.BooleanField('Classificação', default=False, help_text='Classificação da propriedade')


    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'

    def __str__(self):
        return self.nome
    
    def get_status(self):
        return 'Ocupada' if self.classificacao else 'Livre'
    
class chale_comum(Propriedade):
    class Meta:
        verbose_name = 'Chale comum'
        verbose_name_plural = 'Chales comum'

class chale_exclusivo(Propriedade):
    class Meta:
        verbose_name = 'Chale exclusivo'
        verbose_name_plural = 'Chales exclusivos'

