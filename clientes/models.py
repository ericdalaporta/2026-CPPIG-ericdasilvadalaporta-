from django.db import models

class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=70, help_text='Nome do cliente')
    telefone = models.CharField('Telefone', max_length=20, help_text='Telefone do cliente')
    email = models.EmailField('E-mail', max_length=50, help_text='E-mail do cliente', unique=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome