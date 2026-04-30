from django.db import models


class Propriedade(models.Model):
    CLASSIFICACAO_CHOICES = [
        (True, 'Ocupada'),
        (False, 'Livre'),
    ]
    
    nome = models.CharField('Nome', max_length=70, help_text='Nome da propriedade')
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
