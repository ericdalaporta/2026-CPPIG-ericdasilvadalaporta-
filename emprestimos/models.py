from datetime import date

from django.db import models


class Emprestimo(models.Model):

    cliente = models.ForeignKey(
        'clientes.Cliente',
        verbose_name='Cliente',
        help_text='Nome do cliente',
        on_delete=models.PROTECT,
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
        help_text='Indica se o empréstimo está em andamento'
    )

    data_conclusao = models.DateField(
        'Data de Conclusão',
        null=True,
        blank=True,
        help_text='Data em que o empréstimo foi concluído'
    )

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'

    def __str__(self):
        return f'Empréstimo {self.id}'

    def dias_atraso(self):
        """
        Enquanto estiver ativo, usa a data atual.

        Depois de concluído, usa a data de conclusão.
        Dessa forma, a multa para de aumentar.
        """

        if self.ativo:
            data_final = date.today()
        else:
            # Proteção para empréstimos antigos
            data_final = self.data_conclusao or self.data_prevista

        dias = (data_final - self.data_prevista).days

        return max(0, dias)

    def calcular_multa(self):
        """Calcula R$ 200,00 por dia de atraso."""

        return self.dias_atraso() * 200

    def esta_atrasado(self):
        """Retorna True se estiver ativo e atrasado."""

        return self.ativo and self.dias_atraso() > 0

    def get_status(self):
        """Retorna o texto mostrado na tela."""

        if not self.ativo:
            return 'Concluído'

        if self.esta_atrasado():
            return 'Atrasado'

        return 'Em andamento'

    notificacao_atraso = models.BooleanField( '''Notificação de Atraso Enviada''',
        default=False
    )

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
        help_text='Multa final deste item'
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

        unique_together = (
            'emprestimo',
            'copia_chave'
        )

        permissions = (
            (
                'view_item_emprestimo',
                'Pode visualizar itens de empréstimo'
            ),
        )

    def __str__(self):
        return f'Item {self.id} - {self.copia_chave}'

    def calcular_multa(self):
        """
        Enquanto o item não foi devolvido, usa a data atual.

        Depois da devolução, usa a data de devolução e a multa
        deixa de aumentar.
        """

        if self.data_devolucao_item:
            data_final = self.data_devolucao_item

        elif self.emprestimo.ativo:
            data_final = date.today()

        else:
            data_final = (
                self.emprestimo.data_conclusao
                or self.emprestimo.data_prevista
            )

        dias_atraso = (
            data_final - self.emprestimo.data_prevista
        ).days

        return max(0, dias_atraso) * 200