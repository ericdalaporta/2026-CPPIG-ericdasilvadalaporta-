from django.db import models


class Registro(models.Model):
    EVENTO_CHOICES = [
        ('criacao', 'Criação'),
        ('retirada', 'Retirada'),
        ('devolucao', 'Devolução'),
        ('reserva', 'Reserva Agendada'),
        ('alteracao_status', 'Alteração de Status'),
    ]
    
    tipo_evento = models.CharField(max_length=20, choices=EVENTO_CHOICES)
    copia = models.CharField(max_length=255)
    descricao = models.TextField()
    data_evento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ['-data_evento']
    
    def __str__(self):
        return f'{self.get_tipo_evento_display()} - {self.copia} ({self.data_evento})'
