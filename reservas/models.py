from django.db import models

class Reserva(models.Model):
    cliente = models.ForeignKey(
        'clientes.Cliente', 
        verbose_name='Cliente', 
        help_text='Nome do cliente', 
        on_delete=models.PROTECT, 
        related_name='reservas', 
        null=True, 
        blank=True
    )
    
    # ✅ MUDANÇA: De ForeignKey para ManyToManyField
    chaves = models.ManyToManyField(
        'chaves.Chave',
        verbose_name='Chaves',
        help_text='Chaves da reserva',
        related_name='reservas',
        blank=False
    )
    
    data_inicio = models.DateField('Data Início', blank=False, help_text='Data de início da reserva')
    data_fim = models.DateField('Data Fim', blank=False, help_text='Data de término da reserva')
    status = models.CharField('Status', max_length=50, blank=False, help_text='Status da reserva')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva {self.id}'