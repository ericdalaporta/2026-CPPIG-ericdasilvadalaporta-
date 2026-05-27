from django.db import models
from datetime import date

# a lógica eh, um emprestimo pode ter vários 
# ItemEmprestimo apontando pra várias CopiaChave
# e cada ItemEmprestimo tem seu próprio status, multa e data de devolução

class Emprestimo(models.Model):

    cliente = models.ForeignKey(
        'clientes.Cliente',
        verbose_name='Cliente',
        help_text='Nome do cliente',
        on_delete=models.PROTECT, # impedir apagar cliente com empréstimos
        related_name='emprestimos',
        null=True,
        blank=True
    )

    data_retirada = models.DateField(
        'Data de Retirada',
        help_text='Data da retirada do empréstimo'
    )

    data_prevista = models.DateField(
        'Data Prevista',
        help_text='Data prevista de devolução'
    )

    ativo = models.BooleanField(
        'Ativo',
        default=True,
        help_text='Se o empréstimo está em andamento ou concluído'
    )

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'

    def __str__(self):
        return f'Empréstimo {self.id}'

    def dias_atraso(self): # calcula dias de atraso. Se não está ativo, sem atraso.
        if not self.ativo:
            return 0

        dias = (date.today() - self.data_prevista).days
        return max(0, dias)

    def calcular_multa(self):
        return self.dias_atraso() * 200

    def esta_atrasado(self):

        if self.ativo and self.dias_atraso() > 0:
            return True # funcao que indica se o empréstimo está atrasado (ativo e com dias de atraso > 0)

        return False # se nao entrou no if, nao ta atrasado

    def get_status(self): # isso aparece no admin

        if self.ativo:
            return 'Ativo'

        return 'Concluído'


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
        on_delete=models.CASCADE,
        related_name='itens'
    )

    copia_chave = models.ForeignKey(
        'chaves.CopiaChave',
        verbose_name='Cópia de Chave',
        help_text='Cópia de chave emprestada',
        on_delete=models.PROTECT,
        related_name='itens_emprestimo'
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

    data_devolucao_item = models.DateField( # eh usado pra calcular multa, e pra mostrar data de devolução do item
        'Data de Devolução do Item',
        null=True,
        blank=True,
        help_text='Data em que este item foi devolvido'
    )

    class Meta:
        verbose_name = 'Item Empréstimo'
        verbose_name_plural = 'Itens Empréstimos'
        unique_together = ('emprestimo', 'copia_chave')

    def __str__(self):
        return f'Item {self.id} - {self.copia_chave}'

    def calcular_multa(self): #aqui tem outro cálculo de multa, específico pra cada item, baseado na data de devolução do item. 
        # se nao devolveu, calcula com base na data prevista do empréstimo. Se devolveu, calcula com base na data de devolução do item.
        # é necessário porque se um cliente pegar mais de uma copia chave, pode devolver uma antes da data prevista, e outra depois, e a multa tem que ser calculada separada.
        
        if (
            self.data_devolucao_item is None
            and self.emprestimo.data_prevista
        ):
            dias_atraso = (
                date.today() - self.emprestimo.data_prevista
            ).days

            if dias_atraso > 0:
                return dias_atraso * 200

        return 0