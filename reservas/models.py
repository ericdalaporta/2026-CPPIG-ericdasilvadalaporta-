from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Reserva(models.Model):
    STATUS_PENDENTE = 'PENDENTE'
    STATUS_CONFIRMADA = 'CONFIRMADA'
    STATUS_CANCELADA = 'CANCELADA'
    STATUS_FINALIZADA = 'FINALIZADA'
    STATUS_CONVERTIDA = 'CONVERTIDA'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_CONFIRMADA, 'Confirmada'),
        (STATUS_CANCELADA, 'Cancelada'),
        (STATUS_FINALIZADA, 'Finalizada'),
        (STATUS_CONVERTIDA, 'Convertida em Empréstimo'),
    ]

    cliente = models.ForeignKey(
        'clientes.Cliente',
        verbose_name='Cliente',
        help_text='Nome do cliente',
        on_delete=models.PROTECT,
        related_name='reservas',
        null=True,
        blank=True
    )

    chaves = models.ManyToManyField(
        'chaves.Chave',
        verbose_name='Chaves',
        help_text='Chaves da reserva',
        related_name='reservas',
        blank=False
    )

    data_inicio = models.DateTimeField(
        'Data e Hora de Início',
        blank=False,
        help_text='Data e hora de início da reserva'
    )

    data_fim = models.DateTimeField(
        'Data e Hora de Fim',
        blank=False,
        help_text='Data e hora de término da reserva'
    )

    status = models.CharField(
        'Status',
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
        blank=False,
        help_text='Status da reserva'
    )

    observacao = models.TextField(
        'Observação',
        blank=True,
        help_text='Observações internas sobre a reserva'
    )

    emprestimo_gerado = models.ForeignKey(
        'emprestimos.Emprestimo',
        verbose_name='Empréstimo Gerado',
        on_delete=models.SET_NULL,
        related_name='reservas_origem',
        null=True,
        blank=True,
        help_text='Empréstimo criado a partir desta reserva'
    )

    data_cancelamento = models.DateTimeField(
        'Data de Cancelamento',
        null=True,
        blank=True
    )

    data_finalizacao = models.DateTimeField(
        'Data de Finalização',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-data_inicio', '-id']

    def __str__(self):
        if self.cliente:
            return f'Reserva {self.id} - {self.cliente.nome}'
        return f'Reserva {self.id}'

    def clean(self):
        super().clean()

        if not self.cliente_id:
            raise ValidationError({'cliente': 'A reserva precisa ter um cliente.'})

        if self.data_inicio and self.data_fim and self.data_inicio >= self.data_fim:
            raise ValidationError({
                'data_fim': 'A data e hora final precisa ser posterior à data e hora inicial.'
            })

    @property
    def esta_ativa(self):
        return self.status in [
            self.STATUS_PENDENTE,
            self.STATUS_CONFIRMADA,
        ]

    def pode_converter_em_emprestimo(self):
        return self.status in [
            self.STATUS_PENDENTE,
            self.STATUS_CONFIRMADA,
        ]

    def get_status_badge(self):
        if self.status == self.STATUS_CONFIRMADA:
            return 'success'

        if self.status == self.STATUS_PENDENTE:
            return 'warning'

        if self.status == self.STATUS_CANCELADA:
            return 'danger'

        if self.status == self.STATUS_FINALIZADA:
            return 'secondary'

        if self.status == self.STATUS_CONVERTIDA:
            return 'primary'

        return 'secondary'

    def marcar_cancelada(self):
        self.status = self.STATUS_CANCELADA
        self.data_cancelamento = timezone.now()
        self.save(update_fields=['status', 'data_cancelamento'])

    def marcar_finalizada(self):
        self.status = self.STATUS_FINALIZADA
        self.data_finalizacao = timezone.now()
        self.save(update_fields=['status', 'data_finalizacao'])