from django.db import models


class Reserva(models.Model):
    data_inicio = models.DateField('Data Início', blank=False, help_text='Data de início da reserva')
    data_fim = models.DateField('Data Fim', blank=False, help_text='Data de término da reserva')
    status = models.CharField('Status', max_length=50, blank=False, help_text='Status da reserva')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva {self.id}'
