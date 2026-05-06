from django.db import models
from datetime import date


class Emprestimo(models.Model):
  
    cliente = models.ForeignKey(
        'clientes.Cliente', # fk pra cliente dentro de emprestimo
        verbose_name='Cliente', 
        help_text='Nome do cliente', 
        on_delete=models.PROTECT,  # NAO deleta cliente com empréstimos ativos
        related_name='emprestimos',  # Permite cliente.emprestimos.all()
        null=True, 
        blank=True
    )
    
    data_retirada = models.DateField(
        'Data de Retirada', 
        blank=False, 
        help_text='Data da retirada do empréstimo'
    )
    

    data_prevista = models.DateField(
        'Data Prevista', 
        blank=False, 
        help_text='Data prevista de devolução'
    )

    data_devolucao = models.DateField(
        'Data de Devolução', 
        null=True, 
        blank=True, 
        help_text='Data da devolução do empréstimo'
    )

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'

    def __str__(self):
        return f'Empréstimo {self.id}'
    
    def calcular_multa(self):
      
        if self.data_devolucao is None:  # Ainda não devolveu
            dias_atraso = (date.today() - self.data_prevista).days
            if dias_atraso > 0:  # Passou da data prevista
                return dias_atraso * 200  # R$ 200 por dia
        return 0  # Não atrasado
    
    def esta_atrasado(self):
      
        return self.data_devolucao is None and date.today() > self.data_prevista
    
    def dias_atraso(self):
      
        if self.esta_atrasado():
            return (date.today() - self.data_prevista).days
        return 0
    
    def toggle_status(self):
       
        if self.data_devolucao is None:
            self.data_devolucao = date.today()  # Marca como devolvido hoje
        else:
            self.data_devolucao = None  # Volta a pendente
        self.save()
    
    def get_status(self):
       
        return 'Devolvida' if self.data_devolucao else 'Pendente'


class ItemEmprestimo(models.Model):
    
    STATUS_CHOICES = [
        ('EMPRESTADA', 'Emprestada'), 
        ('DEVOLVIDA', 'Devolvida'),     
        ('PERDIDA', 'Perdida'),       
    ]


    emprestimo = models.ForeignKey(
        Emprestimo, 
        verbose_name='Empréstimo', 
        help_text='Empréstimo relacionado', 
        on_delete=models.CASCADE,  # Se apagar empréstimo, apaga itens
        related_name='itens'  # Permite: emprestimo.itens.all()
    )
    
    copia_chave = models.ForeignKey(
        'chaves.CopiaChave', 
        verbose_name='Cópia de Chave', 
        help_text='Cópia de chave emprestada', 
        on_delete=models.PROTECT,  # Não deleta cópia em empréstimo
        related_name='itens_emprestimo'  # Permite: copia.itens_emprestimo.all()
    )
 
    status = models.CharField(
        'Status', 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='EMPRESTADA', 
        help_text='Status do item no empréstimo'
    )
    
    multa = models.FloatField(
        'Multa', 
        default=0, 
        help_text='Multa por atraso deste item'
    )

    valor_restituicao_cobrado = models.FloatField(
        'Valor Restituicão Cobrado', 
        default=0, 
        help_text='Se chave foi perdida, valor cobrado'
    )
    
    data_devolucao_item = models.DateField(
        'Data de Devolução do Item', 
        null=True, 
        blank=True, 
        help_text='Data em que este item foi devolvido'
    )

    class Meta:
        verbose_name = 'Item Empréstimo'
        verbose_name_plural = 'Itens Empréstimos'
        unique_together = ('emprestimo', 'copia_chave')  # Uma cópia uma só vez por empréstimo

    def __str__(self):
        return f'Item {self.id} - {self.copia_chave}'
    
    def calcular_multa(self):
        if self.data_devolucao_item is None and self.emprestimo.data_prevista:
            dias_atraso = (date.today() - self.emprestimo.data_prevista).days
            if dias_atraso > 0:
                return dias_atraso * 200  # R$ 200 por dia
        return 0

