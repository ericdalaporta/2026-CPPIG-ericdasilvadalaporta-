from apscheduler.schedulers.blocking import BlockingScheduler

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from emprestimos.models import Emprestimo


def verificar_atrasos():
    agora = timezone.now()

    emprestimos_possivelmente_atrasados = Emprestimo.objects.select_related(
        'cliente'
    ).filter(
        status=Emprestimo.STATUS_EM_ANDAMENTO,
        ativo=True,
        data_prevista__lt=agora,
        notificacao_atraso=False
    )

    for emprestimo in emprestimos_possivelmente_atrasados:
        if not emprestimo.esta_atrasado():
            continue

        if not emprestimo.cliente or not emprestimo.cliente.email:
            continue

        multa_atual = emprestimo.calcular_multa()
        atraso = emprestimo.get_atraso_formatado()

        try:
            send_mail(
                'Empréstimo atrasado',
                (
                    f'Olá, {emprestimo.cliente.nome}.\n\n'
                    'A devolução do seu empréstimo está atrasada.\n\n'
                    f'Data e hora prevista: {emprestimo.data_prevista.strftime("%d/%m/%Y %H:%M")}\n'
                    f'Tempo de atraso: {atraso}\n'
                    f'Multa atual: R$ {multa_atual:.2f}\n\n'
                    'Por favor, realize a devolução das chaves o quanto antes.'
                ),
                settings.EMAIL_HOST_USER,
                [emprestimo.cliente.email],
                fail_silently=False
            )

            emprestimo.notificacao_atraso = True
            emprestimo.data_notificacao_atraso = agora
            emprestimo.save(update_fields=[
                'notificacao_atraso',
                'data_notificacao_atraso'
            ])

            print(f'E-mail de atraso enviado para empréstimo #{emprestimo.id}.')

        except Exception as erro:
            print(f'Erro ao enviar e-mail do empréstimo #{emprestimo.id}: {erro}')


class Command(BaseCommand):
    help = 'Verifica empréstimos atrasados e envia e-mails de notificação.'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        scheduler.add_job(
            verificar_atrasos,
            'interval',
            minutes=1,
            max_instances=1,
            coalesce=True
        )

        self.stdout.write(self.style.SUCCESS('Scheduler iniciado.'))

        scheduler.start()