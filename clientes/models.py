from django.db import models
from stdimage import StdImageField


class Cliente(models.Model):

    nome = models.CharField(
        'Nome',
        max_length=70,
        help_text='Nome do cliente'
    )
    
    telefone = models.CharField(
        'Telefone', 
        max_length=20, 
        help_text='Telefone do cliente'
    )

    email = models.EmailField(
        'E-mail', 
        max_length=100,
        help_text='E-mail do cliente', 
        unique=True  # evitar duplicacao de email
    )
    
    foto = StdImageField(
        'Foto', 
        upload_to='clientes',  #pastaq q fica salva: media/clientes/...
        delete_orphans=True,  # apaga foto antiga qdo troca por nova
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        permissions = (('view_cliente', 'Pode visualizar clientes'),)

    def __str__(self):
        return self.nome
