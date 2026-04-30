from django.db import models


class Chave(models.Model):
    nome = models.CharField('Nome do modelo da chave', max_length=70, blank=False, help_text='Nome do modelo da chave')
    propriedade = models.ForeignKey('propriedades.Propriedade', verbose_name='Propriedade', help_text='Propriedade relacionada', on_delete=models.PROTECT, related_name='chaves', null=True, blank=True)

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return self.nome


class CopiaChave(models.Model):
    codigo = models.IntegerField('Código', blank=False, help_text='Código da cópia da chave')
    chave = models.ForeignKey(Chave, verbose_name='Chave', help_text='Chave relacionada', on_delete=models.PROTECT, related_name='copias', null=True, blank=True)
    status = models.CharField('Status', max_length=50, blank=False, help_text='Status da cópia da chave')
    valor_restituicao = models.FloatField('Valor Restituição', blank=False, help_text='Valor de restituição da cópia')

    class Meta:
        verbose_name = 'Cópia de Chave'
        verbose_name_plural = 'Cópias de Chaves'

    def __str__(self):
        return f'Cópia {self.codigo}'
