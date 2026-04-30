from django.db import models


class Chave(models.Model):
    nome = models.CharField('Nome', max_length=70, blank=False, help_text='Nome da chave')

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return self.nome


class CopiaChave(models.Model):
    codigo = models.IntegerField('Código', blank=False, help_text='Código da cópia da chave')
    status = models.CharField('Status', max_length=50, blank=False, help_text='Status da cópia da chave')
    valor_restituicao = models.FloatField('Valor Restituição', blank=False, help_text='Valor de restituição da cópia')

    class Meta:
        verbose_name = 'Cópia de Chave'
        verbose_name_plural = 'Cópias de Chaves'

    def __str__(self):
        return f'Cópia {self.codigo}'
