from django.db import models
from propriedades.models import Propriedade


class Chave(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('emprestada', 'Emprestada'),
        ('reservada', 'Reservada'),
        ('manutencao', 'Manutenção'),
        ('perdida', 'Perdida'),
    ]
    
    nome = models.CharField(max_length=255)
    id_fisico = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    propriedade = models.ForeignKey(Propriedade, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'
    
    def __str__(self):
        return f'{self.nome} ({self.id_fisico})'
