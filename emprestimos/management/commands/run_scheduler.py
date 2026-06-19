from datetime import date

from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from emprestimos.models import Emprestimo


def verificar_atrasos():

    emprestimos_atrasados = Emprestimo.objects.filter(
        ativo=True,
        data_prevista__lt=date.today(),
        notificacao_atraso=False
    )

    for emprestimo in emprestimos_atrasados:

        send_mail(
            'Empréstimo atrasado',
            (
                f'Olá, {emprestimo.cliente.nome}.\n\n'
                'A devolução do seu empréstimo está atrasada.\n'
                'A multa é de R$ 200,00 por dia de atraso.'
            ),
            settings.EMAIL_HOST_USER,
            [emprestimo.cliente.email]
        )

        emprestimo.notificacao_atraso = True
        emprestimo.save()


class Command(BaseCommand):

    def handle(self, *args, **options):

        scheduler = BlockingScheduler()

        scheduler.add_job(
            verificar_atrasos,
            'interval',
            minutes=1
        )

        print('Scheduler iniciado.')

        scheduler.start()