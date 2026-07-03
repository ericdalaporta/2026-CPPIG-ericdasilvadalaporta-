from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from chaves.models import CopiaChave
from .models import Emprestimo, ItemEmprestimo


class RegraEmprestimoError(ValidationError):
    pass


def status_copia(nome, padrao):
    return getattr(CopiaChave, nome, padrao)


def salvar_status_copia(copia, novo_status, data_perda=None):
    copia.status = novo_status

    update_fields = ['status']

    if hasattr(copia, 'data_perda'):
        if novo_status == status_copia('STATUS_PERDIDA', 'PERDIDA'):
            copia.data_perda = data_perda or timezone.now()
        else:
            copia.data_perda = None

        update_fields.append('data_perda')

    copia.save(update_fields=update_fields)


def normalizar_ids_copias(copias_selecionadas):
    ids = []
    vistos = set()

    for valor in copias_selecionadas:
        if valor in (None, ''):
            continue

        try:
            copia_id = int(valor)
        except (TypeError, ValueError):
            raise RegraEmprestimoError('Uma das cópias selecionadas é inválida.')

        if copia_id not in vistos:
            vistos.add(copia_id)
            ids.append(copia_id)

    return ids


def validar_datas_emprestimo(emprestimo):
    if not emprestimo.cliente:
        raise RegraEmprestimoError('Selecione o cliente do empréstimo.')

    if emprestimo.data_retirada >= emprestimo.data_prevista:
        raise RegraEmprestimoError(
            'A data e hora prevista precisa ser posterior à data e hora de retirada.'
        )


def adicionar_copias_portao(ids_copias):
    ids_copias = normalizar_ids_copias(ids_copias)

    if not ids_copias:
        return ids_copias

    status_disponivel = status_copia('STATUS_DISPONIVEL', 'DISPONIVEL')

    copias = CopiaChave.objects.select_related(
        'chave__propriedade__portao_associado'
    ).filter(id__in=ids_copias)

    for copia in copias:
        propriedade = copia.chave.propriedade

        if not propriedade:
            continue

        if propriedade.tipo != 'CHALE_EXCLUSIVO':
            continue

        if not propriedade.portao_associado_id:
            continue

        portao = propriedade.portao_associado

        portao_ja_incluido = CopiaChave.objects.filter(
            id__in=ids_copias,
            chave__propriedade=portao
        ).exists()

        if portao_ja_incluido:
            continue

        copia_portao = CopiaChave.objects.select_for_update().filter(
            chave__propriedade=portao,
            status=status_disponivel
        ).first()

        if copia_portao is None:
            raise RegraEmprestimoError(
                f'O chalé {propriedade.nome} exige chave do portão, '
                f'mas não existe cópia disponível do portão {portao.nome}.'
            )

        ids_copias.append(copia_portao.id)

    return normalizar_ids_copias(ids_copias)


def buscar_e_validar_copias_para_emprestimo(ids_copias, ids_copias_atuais=None):
    ids_copias = normalizar_ids_copias(ids_copias)
    ids_copias_atuais = set(ids_copias_atuais or [])

    if not ids_copias:
        raise RegraEmprestimoError('Selecione pelo menos uma cópia de chave.')

    copias = list(
        CopiaChave.objects.select_for_update()
        .select_related('chave__propriedade')
        .filter(id__in=ids_copias)
    )

    if len(copias) != len(ids_copias):
        raise RegraEmprestimoError('Uma ou mais cópias selecionadas não existem mais.')

    copias_por_id = {copia.id: copia for copia in copias}
    copias_ordenadas = [copias_por_id[copia_id] for copia_id in ids_copias]

    status_disponivel = status_copia('STATUS_DISPONIVEL', 'DISPONIVEL')

    for copia in copias_ordenadas:
        if copia.id in ids_copias_atuais:
            continue

        if copia.status != status_disponivel:
            raise RegraEmprestimoError(
                f'A cópia {copia.codigo} da chave {copia.chave.nome} não está disponível.'
            )

    return copias_ordenadas


def criar_itens_emprestimo(emprestimo, copias):
    status_emprestada = status_copia('STATUS_EMPRESTADA', 'EMPRESTADA')

    for copia in copias:
        ItemEmprestimo.objects.create(
            emprestimo=emprestimo,
            copia_chave=copia,
            status=ItemEmprestimo.STATUS_EMPRESTADA
        )

        salvar_status_copia(copia, status_emprestada)


def sincronizar_multa_itens(emprestimo):
    multa_total = emprestimo.calcular_multa()
    itens = list(emprestimo.itens.all())

    if not itens:
        return

    multa_por_item = multa_total / Decimal(len(itens))

    for item in itens:
        item.multa = multa_por_item
        item.save(update_fields=['multa'])


def devolver_itens(emprestimo, data_devolucao=None):
    data_devolucao = data_devolucao or timezone.now()

    status_disponivel = status_copia('STATUS_DISPONIVEL', 'DISPONIVEL')
    status_perdida = status_copia('STATUS_PERDIDA', 'PERDIDA')

    for item in emprestimo.itens.select_related('copia_chave').select_for_update():
        copia = item.copia_chave

        if item.status == ItemEmprestimo.STATUS_PERDIDA:
            salvar_status_copia(copia, status_perdida, data_perda=data_devolucao)
            continue

        item.status = ItemEmprestimo.STATUS_DEVOLVIDA
        item.data_devolucao_item = data_devolucao
        item.save(update_fields=['status', 'data_devolucao_item'])

        salvar_status_copia(copia, status_disponivel)


def criar_emprestimo(emprestimo, ids_copias, incluir_portao=False):
    with transaction.atomic():
        validar_datas_emprestimo(emprestimo)

        if incluir_portao:
            ids_copias = adicionar_copias_portao(ids_copias)
        else:
            ids_copias = normalizar_ids_copias(ids_copias)

        copias = buscar_e_validar_copias_para_emprestimo(ids_copias)

        emprestimo.status = Emprestimo.STATUS_EM_ANDAMENTO
        emprestimo.ativo = True
        emprestimo.data_conclusao = None
        emprestimo.data_cancelamento = None
        emprestimo.motivo_cancelamento = ''
        emprestimo.save()

        criar_itens_emprestimo(emprestimo, copias)

        return emprestimo


def atualizar_emprestimo(emprestimo, ids_copias, incluir_portao=False):
    with transaction.atomic():
        emprestimo_antigo = Emprestimo.objects.select_for_update().get(pk=emprestimo.pk)

        if emprestimo_antigo.status != Emprestimo.STATUS_EM_ANDAMENTO:
            raise RegraEmprestimoError('Somente empréstimos em andamento podem ser editados.')

        validar_datas_emprestimo(emprestimo)

        ids_copias_atuais = set(
            emprestimo_antigo.itens.select_for_update().values_list('copia_chave_id', flat=True)
        )

        if incluir_portao:
            ids_copias = adicionar_copias_portao(ids_copias)
        else:
            ids_copias = normalizar_ids_copias(ids_copias)

        copias_novas = buscar_e_validar_copias_para_emprestimo(
            ids_copias,
            ids_copias_atuais=ids_copias_atuais
        )

        ids_novos = {copia.id for copia in copias_novas}

        status_disponivel = status_copia('STATUS_DISPONIVEL', 'DISPONIVEL')
        status_emprestada = status_copia('STATUS_EMPRESTADA', 'EMPRESTADA')

        itens_removidos = emprestimo_antigo.itens.exclude(copia_chave_id__in=ids_novos)

        for item in itens_removidos.select_related('copia_chave'):
            copia = item.copia_chave
            status_item = item.status

            item.delete()

            if status_item != ItemEmprestimo.STATUS_PERDIDA:
                salvar_status_copia(copia, status_disponivel)

        for copia in copias_novas:
            item, criado = ItemEmprestimo.objects.get_or_create(
                emprestimo=emprestimo_antigo,
                copia_chave=copia,
                defaults={'status': ItemEmprestimo.STATUS_EMPRESTADA}
            )

            if criado or item.status != ItemEmprestimo.STATUS_EMPRESTADA:
                item.status = ItemEmprestimo.STATUS_EMPRESTADA
                item.data_devolucao_item = None
                item.data_perda_item = None
                item.save(update_fields=['status', 'data_devolucao_item', 'data_perda_item'])

            salvar_status_copia(copia, status_emprestada)

        emprestimo_antigo.cliente = emprestimo.cliente
        emprestimo_antigo.data_retirada = emprestimo.data_retirada
        emprestimo_antigo.data_prevista = emprestimo.data_prevista
        emprestimo_antigo.valor_multa_por_hora = emprestimo.valor_multa_por_hora
        emprestimo_antigo.tolerancia_minutos = emprestimo.tolerancia_minutos
        emprestimo_antigo.save()

        return emprestimo_antigo


def concluir_emprestimo(emprestimo, data_conclusao=None):
    data_conclusao = data_conclusao or timezone.now()

    with transaction.atomic():
        emprestimo = Emprestimo.objects.select_for_update().get(pk=emprestimo.pk)

        if emprestimo.status == Emprestimo.STATUS_CANCELADO:
            raise RegraEmprestimoError('Não é possível concluir um empréstimo cancelado.')

        if emprestimo.status == Emprestimo.STATUS_CONCLUIDO:
            return emprestimo

        emprestimo.status = Emprestimo.STATUS_CONCLUIDO
        emprestimo.data_conclusao = data_conclusao
        emprestimo.ativo = False
        emprestimo.save(update_fields=['status', 'data_conclusao', 'ativo'])

        devolver_itens(emprestimo, data_devolucao=data_conclusao)
        sincronizar_multa_itens(emprestimo)

        return emprestimo


def cancelar_emprestimo(emprestimo, motivo='Cancelado pelo usuário do sistema.'):
    with transaction.atomic():
        emprestimo = Emprestimo.objects.select_for_update().get(pk=emprestimo.pk)

        if emprestimo.status == Emprestimo.STATUS_CONCLUIDO:
            raise RegraEmprestimoError('Não é possível cancelar um empréstimo já concluído.')

        if emprestimo.status == Emprestimo.STATUS_CANCELADO:
            return emprestimo

        agora = timezone.now()

        emprestimo.status = Emprestimo.STATUS_CANCELADO
        emprestimo.data_cancelamento = agora
        emprestimo.motivo_cancelamento = motivo
        emprestimo.ativo = False
        emprestimo.save(update_fields=[
            'status',
            'data_cancelamento',
            'motivo_cancelamento',
            'ativo'
        ])

        devolver_itens(emprestimo, data_devolucao=agora)

        return emprestimo


def marcar_item_como_perdido(item, observacao=''):
    with transaction.atomic():
        item = ItemEmprestimo.objects.select_for_update().select_related(
            'emprestimo',
            'copia_chave'
        ).get(pk=item.pk)

        if item.emprestimo.status != Emprestimo.STATUS_EM_ANDAMENTO:
            raise RegraEmprestimoError('Só é possível marcar perda em empréstimo em andamento.')

        if item.status == ItemEmprestimo.STATUS_PERDIDA:
            return item

        if item.status == ItemEmprestimo.STATUS_DEVOLVIDA:
            raise RegraEmprestimoError('Não é possível marcar como perdida uma cópia já devolvida.')

        agora = timezone.now()

        valor_restituicao = getattr(
            item.copia_chave,
            'valor_restituicao',
            Decimal('100.00')
        )

        item.status = ItemEmprestimo.STATUS_PERDIDA
        item.data_perda_item = agora
        item.valor_cobranca_perda = valor_restituicao
        item.observacao = observacao or item.observacao
        item.save(update_fields=[
            'status',
            'data_perda_item',
            'valor_cobranca_perda',
            'observacao'
        ])

        status_perdida = status_copia('STATUS_PERDIDA', 'PERDIDA')
        salvar_status_copia(item.copia_chave, status_perdida, data_perda=agora)

        return item