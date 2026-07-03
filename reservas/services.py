from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from chaves.models import CopiaChave
from emprestimos.models import Emprestimo, ItemEmprestimo
from emprestimos.services import criar_emprestimo, RegraEmprestimoError
from .models import Reserva


class RegraReservaError(ValidationError):
    pass


def intervalos_conflitam(inicio_1, fim_1, inicio_2, fim_2):
    return inicio_1 < fim_2 and fim_1 > inicio_2


def validar_datas_reserva(reserva):
    if not reserva.cliente:
        raise RegraReservaError('Selecione o cliente da reserva.')

    if reserva.data_inicio >= reserva.data_fim:
        raise RegraReservaError(
            'A data e hora final precisa ser posterior à data e hora inicial.'
        )


def buscar_conflitos_reserva(chaves, data_inicio, data_fim, reserva_id=None):
    reservas = Reserva.objects.filter(
        chaves__in=chaves,
        data_inicio__lt=data_fim,
        data_fim__gt=data_inicio,
        status__in=[
            Reserva.STATUS_PENDENTE,
            Reserva.STATUS_CONFIRMADA,
        ]
    )

    if reserva_id:
        reservas = reservas.exclude(pk=reserva_id)

    return reservas.distinct()


def buscar_conflitos_emprestimo(chaves, data_inicio, data_fim):
    return Emprestimo.objects.filter(
        status=Emprestimo.STATUS_EM_ANDAMENTO,
        data_retirada__lt=data_fim,
        data_prevista__gt=data_inicio,
        itens__status=ItemEmprestimo.STATUS_EMPRESTADA,
        itens__copia_chave__chave__in=chaves
    ).distinct()


def validar_conflitos_reserva(reserva, chaves):
    if not chaves:
        raise RegraReservaError('Selecione pelo menos uma chave para a reserva.')

    if reserva.status in [
        Reserva.STATUS_CANCELADA,
        Reserva.STATUS_FINALIZADA,
        Reserva.STATUS_CONVERTIDA,
    ]:
        return

    conflitos_reserva = buscar_conflitos_reserva(
        chaves,
        reserva.data_inicio,
        reserva.data_fim,
        reserva_id=reserva.pk if reserva.pk else None
    )

    if conflitos_reserva.exists():
        ids = ', '.join(str(reserva.id) for reserva in conflitos_reserva[:5])
        raise RegraReservaError(
            f'Existe conflito com outra reserva ativa nesse período. Reserva(s): {ids}.'
        )

    conflitos_emprestimo = buscar_conflitos_emprestimo(
        chaves,
        reserva.data_inicio,
        reserva.data_fim
    )

    if conflitos_emprestimo.exists():
        ids = ', '.join(str(emprestimo.id) for emprestimo in conflitos_emprestimo[:5])
        raise RegraReservaError(
            f'Existe chave emprestada nesse período. Empréstimo(s): {ids}.'
        )


def cancelar_reserva(reserva):
    with transaction.atomic():
        reserva = Reserva.objects.select_for_update().get(pk=reserva.pk)

        if reserva.status == Reserva.STATUS_CONVERTIDA:
            raise RegraReservaError(
                'Não é possível cancelar uma reserva que já foi convertida em empréstimo.'
            )

        if reserva.status == Reserva.STATUS_FINALIZADA:
            raise RegraReservaError(
                'Não é possível cancelar uma reserva já finalizada.'
            )

        if reserva.status == Reserva.STATUS_CANCELADA:
            return reserva

        reserva.status = Reserva.STATUS_CANCELADA
        reserva.data_cancelamento = timezone.now()
        reserva.save(update_fields=['status', 'data_cancelamento'])

        return reserva


def finalizar_reserva(reserva):
    with transaction.atomic():
        reserva = Reserva.objects.select_for_update().get(pk=reserva.pk)

        if reserva.status == Reserva.STATUS_CANCELADA:
            raise RegraReservaError('Não é possível finalizar uma reserva cancelada.')

        if reserva.status == Reserva.STATUS_CONVERTIDA:
            raise RegraReservaError(
                'Não é possível finalizar uma reserva que já virou empréstimo.'
            )

        if reserva.status == Reserva.STATUS_FINALIZADA:
            return reserva

        reserva.status = Reserva.STATUS_FINALIZADA
        reserva.data_finalizacao = timezone.now()
        reserva.save(update_fields=['status', 'data_finalizacao'])

        return reserva


def buscar_copias_disponiveis_para_chaves(chaves):
    ids_copias = []

    status_disponivel = getattr(CopiaChave, 'STATUS_DISPONIVEL', 'DISPONIVEL')

    for chave in chaves:
        copia = CopiaChave.objects.select_for_update().filter(
            chave=chave,
            status=status_disponivel
        ).first()

        if copia is None:
            raise RegraReservaError(
                f'Não existe cópia disponível para a chave {chave.nome}.'
            )

        ids_copias.append(copia.id)

    return ids_copias


def converter_reserva_em_emprestimo(reserva):
    with transaction.atomic():
        reserva = Reserva.objects.select_for_update().prefetch_related('chaves').get(
            pk=reserva.pk
        )

        if not reserva.pode_converter_em_emprestimo():
            raise RegraReservaError(
                'Somente reservas pendentes ou confirmadas podem virar empréstimo.'
            )

        chaves = list(reserva.chaves.all())

        validar_datas_reserva(reserva)
        validar_conflitos_reserva(reserva, chaves)

        ids_copias = buscar_copias_disponiveis_para_chaves(chaves)

        emprestimo = Emprestimo(
            cliente=reserva.cliente,
            data_retirada=reserva.data_inicio,
            data_prevista=reserva.data_fim
        )

        try:
            emprestimo = criar_emprestimo(
                emprestimo,
                ids_copias,
                incluir_portao=True
            )
        except RegraEmprestimoError as erro:
            raise RegraReservaError(erro.messages)

        reserva.status = Reserva.STATUS_CONVERTIDA
        reserva.emprestimo_gerado = emprestimo
        reserva.save(update_fields=['status', 'emprestimo_gerado'])

        return emprestimo