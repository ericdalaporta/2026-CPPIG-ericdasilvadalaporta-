from django.db import models


class Chave(models.Model):
    
    nome = models.CharField(
        'Nome do modelo da chave', 
        max_length=70, 
        blank=False, 
        help_text='Nome do modelo da chave'
    )

    propriedade = models.ForeignKey( #da pra cadastrar 1 chave pra mais de 1 prop no
        #front mas não no mesmo form!!!!
        'propriedades.Propriedade',
        verbose_name='Propriedade', 
        help_text='Propriedade relacionada', 
        on_delete=models.PROTECT,
        related_name='chaves',
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return self.nome


class CopiaChave(models.Model):
    
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('EMPRESTADA', 'Emprestada'),
        ('PERDIDA', 'Perdida'),
    ]

    codigo = models.IntegerField( #pegar numero inteiro
        'Código', 
        blank=False, 
        help_text='Código da cópia da chave'
    )
    
    chave = models.ForeignKey( #mesma coisa que aquele caso da chave com propriedade
        Chave,
        verbose_name='Chave', 
        help_text='Chave relacionada', 
        on_delete=models.PROTECT,
        related_name='copias',
        null=True, 
        blank=True
    )
    
    status = models.CharField( #choice de disponibilidade da cópia
        'Status', 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='DISPONIVEL',
        blank=False, 
        help_text='Status da cópia da chave'
    )
    
    valor_restituicao = models.FloatField(
        'Valor Restituição', 
        blank=False, 
        help_text='Valor de restituição da cópia'
    )

    class Meta:
        verbose_name = 'Cópia de Chave'
        verbose_name_plural = 'Cópias de Chaves'

    def __str__(self):
        return f'Cópia {self.codigo}'