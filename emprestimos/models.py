from decimal import Decimal, ROUND_CEILING

from django.db import models
from django.utils import timezone


class Emprestimo(models.Model):
    STATUS_EM_ANDAMENTO = 'EM_ANDAMENTO'
    STATUS_CONCLUIDO = 'CONCLUIDO'
    STATUS_CANCELADO = 'CANCELADO'

    STATUS_CHOICES = [
        (STATUS_EM_ANDAMENTO, 'Em andamento'),
        (STATUS_CONCLUIDO, 'Concluído'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        'clientes.Cliente',
        verbose_name='Cliente',
        help_text='Nome do cliente',
        on_delete=models.PROTECT,
        related_name='emprestimos',
        null=True,
        blank=True
    )

    data_retirada = models.DateTimeField(
        'Data e Hora de Retirada',
        help_text='Data e hora da retirada do empréstimo'
    )

    data_prevista = models.DateTimeField(
        'Data e Hora Prevista',
        help_text='Data e hora prevista de devolução'
    )

    data_conclusao = models.DateTimeField(
        'Data e Hora de Conclusão',
        null=True,
        blank=True,
        help_text='Data e hora em que o empréstimo foi concluído'
    )

    data_cancelamento = models.DateTimeField(
        'Data e Hora de Cancelamento',
        null=True,
        blank=True,
        help_text='Data e hora em que o empréstimo foi cancelado'
    )

    motivo_cancelamento = models.TextField(
        'Motivo do Cancelamento',
        null=True,
        blank=True,
        help_text='Motivo do cancelamento do empréstimo'
    )

    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_EM_ANDAMENTO
    )

    ativo = models.BooleanField(
        'Ativo',
        default=True,
        help_text='Indica se o empréstimo está em andamento'
    )

    valor_multa_por_hora = models.DecimalField(
        'Valor da Multa por Hora',
        max_digits=8,
        decimal_places=2,
        default=Decimal('20.00'),
        help_text='Valor cobrado por hora de atraso'
    )

    tolerancia_minutos = models.PositiveIntegerField(
        'Tolerância em Minutos',
        default=15,
        help_text='Tempo de tolerância antes de começar a contar multa'
    )

    notificacao_atraso = models.BooleanField(
        'Notificação de Atraso Enviada',
        default=False
    )

    data_notificacao_atraso = models.DateTimeField(
        'Data da Notificação de Atraso',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-id']

    def __str__(self):
        if self.cliente:
            return f'Empréstimo {self.id} - {self.cliente.nome}'
        return f'Empréstimo {self.id}'

    def data_final_para_calculo(self):
        if self.status == self.STATUS_CONCLUIDO and self.data_conclusao:
            return self.data_conclusao

        if self.status == self.STATUS_CANCELADO and self.data_cancelamento:
            return self.data_cancelamento

        return timezone.now()

    def tempo_atraso(self):
        data_final = self.data_final_para_calculo()

        diferenca = data_final - self.data_prevista

        segundos_tolerancia = self.tolerancia_minutos * 60
        segundos_atraso = diferenca.total_seconds() - segundos_tolerancia

        if segundos_atraso <= 0:
            return 0

        return int(segundos_atraso)

    def horas_atraso(self):
        segundos = self.tempo_atraso()

        if segundos <= 0:
            return 0

        horas = Decimal(segundos) / Decimal(3600)

        return int(horas.to_integral_value(rounding=ROUND_CEILING))

    def dias_atraso(self):
        segundos = self.tempo_atraso()

        if segundos <= 0:
            return 0

        return segundos // 86400

    def calcular_multa(self):
        horas = self.horas_atraso()

        if horas <= 0:
            return Decimal('0.00')

        return Decimal(horas) * self.valor_multa_por_hora

    def esta_atrasado(self):
        return self.status == self.STATUS_EM_ANDAMENTO and self.tempo_atraso() > 0

    def get_status(self):
        if self.status == self.STATUS_CANCELADO:
            return 'Cancelado'

        if self.status == self.STATUS_CONCLUIDO:
            return 'Concluído'

        if self.esta_atrasado():
            return 'Atrasado'

        return 'Em andamento'

    def get_status_badge(self):
        if self.status == self.STATUS_CANCELADO:
            return 'secondary'

        if self.status == self.STATUS_CONCLUIDO:
            return 'success'

        if self.esta_atrasado():
            return 'danger'

        return 'warning'

    def get_atraso_formatado(self):
        segundos = self.tempo_atraso()

        if segundos <= 0:
            return 'Sem atraso'

        horas = segundos // 3600
        minutos = (segundos % 3600) // 60

        if horas and minutos:
            return f'{horas}h {minutos}min'

        if horas:
            return f'{horas}h'

        return f'{minutos}min'


class ItemEmprestimo(models.Model):
    STATUS_EMPRESTADA = 'EMPRESTADA'
    STATUS_DEVOLVIDA = 'DEVOLVIDA'
    STATUS_PERDIDA = 'PERDIDA'

    STATUS_CHOICES = [
        (STATUS_EMPRESTADA, 'Emprestada'),
        (STATUS_DEVOLVIDA, 'Devolvida'),
        (STATUS_PERDIDA, 'Perdida'),
    ]

    emprestimo = models.ForeignKey(
        Emprestimo,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    copia_chave = models.ForeignKey(
        'chaves.CopiaChave',
        on_delete=models.PROTECT,
        related_name='itens_emprestimo'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_EMPRESTADA
    )

    data_devolucao_item = models.DateTimeField(
        'Data e Hora de Devolução do Item',
        null=True,
        blank=True
    )

    data_perda_item = models.DateTimeField(
        'Data e Hora da Perda',
        null=True,
        blank=True
    )

    multa = models.DecimalField(
        'Multa',
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00')
    )

    valor_cobranca_perda = models.DecimalField(
        'Valor de Cobrança por Perda',
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00')
    )

    observacao = models.TextField(
        'Observação',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Item Empréstimo'
        verbose_name_plural = 'Itens Empréstimos'
        unique_together = (
            'emprestimo',
            'copia_chave'
        )

    def __str__(self):
        return f'Item {self.id} - {self.copia_chave}'

    def get_status_badge(self):
        if self.status == self.STATUS_DEVOLVIDA:
            return 'success'

        if self.status == self.STATUS_PERDIDA:
            return 'danger'

        return 'warning'