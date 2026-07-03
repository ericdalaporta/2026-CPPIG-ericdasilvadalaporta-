from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Chave(models.Model):

    nome = models.CharField(
        'Nome do modelo da chave',
        max_length=70,
        blank=False,
        help_text='Nome do modelo da chave'
    )

    propriedade = models.ForeignKey(
        'propriedades.Propriedade',
        verbose_name='Propriedade',
        help_text='Propriedade relacionada',
        on_delete=models.PROTECT,
        related_name='chaves',
    )

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'
        ordering = ['propriedade__nome', 'nome']

    def __str__(self):
        if self.propriedade_id:
            return f'{self.nome} - {self.propriedade.nome}'

        return self.nome

    @property
    def copias_disponiveis(self):
        return self.copias.filter(status=CopiaChave.STATUS_DISPONIVEL)

    @property
    def quantidade_copias_disponiveis(self):
        return self.copias.filter(status=CopiaChave.STATUS_DISPONIVEL).count()

    @property
    def quantidade_copias_emprestadas(self):
        return self.copias.filter(status=CopiaChave.STATUS_EMPRESTADA).count()

    @property
    def quantidade_copias_perdidas(self):
        return self.copias.filter(status=CopiaChave.STATUS_PERDIDA).count()

    def clean(self):
        super().clean()

        if self.pk:
            chave_antiga = Chave.objects.filter(pk=self.pk).first()

            if chave_antiga and chave_antiga.propriedade_id != self.propriedade_id:
                tem_copia_emprestada = self.copias.filter(
                    status=CopiaChave.STATUS_EMPRESTADA
                ).exists()

                if tem_copia_emprestada:
                    raise ValidationError({
                        'propriedade': 'Não é possível trocar a propriedade de uma chave com cópias emprestadas.'
                    })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class CopiaChave(models.Model):

    STATUS_DISPONIVEL = 'DISPONIVEL'
    STATUS_EMPRESTADA = 'EMPRESTADA'
    STATUS_PERDIDA = 'PERDIDA'
    STATUS_MANUTENCAO = 'MANUTENCAO'
    STATUS_INATIVA = 'INATIVA'

    STATUS_CHOICES = [
        (STATUS_DISPONIVEL, 'Disponível'),
        (STATUS_EMPRESTADA, 'Emprestada'),
        (STATUS_PERDIDA, 'Perdida'),
        (STATUS_MANUTENCAO, 'Em manutenção'),
        (STATUS_INATIVA, 'Inativa'),
    ]

    codigo = models.IntegerField(
        'Código',
        blank=False,
        help_text='Código da cópia da chave'
    )

    chave = models.ForeignKey(
        Chave,
        verbose_name='Chave',
        help_text='Chave relacionada',
        on_delete=models.PROTECT,
        related_name='copias',
    )

    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DISPONIVEL,
        blank=False,
        help_text='Status da cópia da chave'
    )

    valor_restituicao = models.DecimalField(
        'Valor de restituição',
        max_digits=8,
        decimal_places=2,
        default=Decimal('100.00'),
        help_text='Valor cobrado caso esta cópia seja perdida'
    )

    data_perda = models.DateTimeField(
        'Data e hora da perda',
        null=True,
        blank=True,
        help_text='Data e hora em que a cópia foi marcada como perdida'
    )

    observacao = models.TextField(
        'Observação',
        blank=True,
        help_text='Observações internas sobre esta cópia'
    )

    class Meta:
        verbose_name = 'Cópia de Chave'
        verbose_name_plural = 'Cópias de Chaves'
        ordering = ['chave__nome', 'codigo']

    def __str__(self):
        return f'Cópia {self.codigo} - {self.chave.nome}'

    @property
    def esta_disponivel_para_emprestimo(self):
        return self.status == self.STATUS_DISPONIVEL

    @property
    def esta_emprestada(self):
        return self.status == self.STATUS_EMPRESTADA

    @property
    def esta_perdida(self):
        return self.status == self.STATUS_PERDIDA

    def get_status_badge(self):
        if self.status == self.STATUS_DISPONIVEL:
            return 'success'

        if self.status == self.STATUS_EMPRESTADA:
            return 'warning'

        if self.status == self.STATUS_PERDIDA:
            return 'danger'

        if self.status == self.STATUS_MANUTENCAO:
            return 'info'

        if self.status == self.STATUS_INATIVA:
            return 'secondary'

        return 'secondary'

    def clean(self):
        super().clean()

        if self.valor_restituicao is not None and self.valor_restituicao < 0:
            raise ValidationError({
                'valor_restituicao': 'O valor de restituição não pode ser negativo.'
            })

        if self.pk and self.status == self.STATUS_DISPONIVEL:
            existe_emprestimo_ativo = self.itens_emprestimo.filter(
                status='EMPRESTADA',
                emprestimo__status='EM_ANDAMENTO',
                emprestimo__ativo=True
            ).exists()

            if existe_emprestimo_ativo:
                raise ValidationError({
                    'status': 'Esta cópia está em um empréstimo ativo e não pode ficar disponível.'
                })

        if self.status == self.STATUS_PERDIDA and not self.data_perda:
            self.data_perda = timezone.now()

        if self.status != self.STATUS_PERDIDA:
            self.data_perda = None

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)