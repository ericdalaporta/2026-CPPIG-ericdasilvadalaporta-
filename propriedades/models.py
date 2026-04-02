from django.db import models


class Propriedade(models.Model):
    CLASSIFICACAO_CHOICES = [
        ('comum', 'Comum'),
        ('comunitaria', 'Comunitária'),
    ]
    
    nome = models.CharField(max_length=255)
    classificacao = models.CharField(max_length=20, choices=CLASSIFICACAO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'
    
    def __str__(self):
        return self.nome
