from datetime import date

from django.db import models


class Emprestimo(models.Model):

    cliente = models.ForeignKey( # diz que um cliente pode ter vários empréstimos
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
        
        # enquanto estiver ativo, usa a data atual. depois de concluído,
        # usa a data de conclusão, dessa forma, a multa para de aumentar
        

        if self.ativo: # se o emprestimo ainda ta ativo, usa a data de hoje
            data_final = date.today()
        else:
            # se nao ta ativo, foi concluido, daí usa
            # data_conclusao, se nao tiver data_conclusao, usa data_prevista
            data_final = self.data_conclusao or self.data_prevista
            # bota o valor pra dentro de data_final, se data_conclusao for None, usa data_prevista

        dias = (data_final - self.data_prevista).days
        # depois faz a diferença entre a data_final e a data_prevista, pega os dias de diferença
        
        return max(0, dias) #aí retorna aqui a quantridade de dias de atraso

    def calcular_multa(self):

        return self.dias_atraso() * 200 # usei a funcao dias_atraso e multipliquei pela diaria

    def esta_atrasado(self): 
        # retorna true se emprestimo estiver ativo e , eh usado pra mostrar o status do emprestimo na tabela de emprestimos

        return self.ativo and self.dias_atraso() > 0 

    def get_status(self):
        # retorna o texto do status do emprestimo

        if not self.ativo:
            return 'Concluído'

        if self.esta_atrasado():
            return 'Atrasado'

        return 'Em andamento'

    notificacao_atraso = models.BooleanField( "Notificação de Atraso Enviada",
        default=False
    ) # controla o envio do email de notificação de atraso, pra não enviar várias vezes
    # no scheduler, ele procura apenas emprestimos com notificacao_atraso = False, e envia o email, depois muda pra True, pra não enviar de novo

class ItemEmprestimo(models.Model): # representa uma copia dentro de um empréstimo

    STATUS_CHOICES = [ # valor vai pro banco, o segundo pro usuário (não implementado ainda)
        ('EMPRESTADA', 'Emprestada'),
        ('DEVOLVIDA', 'Devolvida'),
        ('PERDIDA', 'Perdida'),
    ]

    emprestimo = models.ForeignKey( # diz que um emprestimo pode ter vários itens, e cada item pertence a um emprestimo
        Emprestimo,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    copia_chave = models.ForeignKey( # diz que uma copia de chave pode estar em vários itens de emprestimo, e cada item pertence a uma copia de chave
        'chaves.CopiaChave',
        on_delete=models.PROTECT,
        related_name='itens_emprestimo'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='EMPRESTADA'
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
    
    multa = models.FloatField( # guarda a multa daquela copia dentro do emprestimo
                              # nem isso nem o campo abaixo precisa estar no trabalho final
                              # pq todas as copias sao entregues juntas
    default=0
    )

    data_devolucao_item = models.DateField(
    null=True,
    blank=True
    )