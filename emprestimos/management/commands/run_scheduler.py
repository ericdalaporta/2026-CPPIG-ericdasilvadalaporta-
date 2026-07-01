from datetime import date

from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from emprestimos.models import Emprestimo


def verificar_atrasos():

    emprestimos_atrasados = Emprestimo.objects.filter( # aqui ele ve o banco de dados e pega todos os emprestimos que estão atrasados, 
        # ou seja, que ainda estão ativos, a data prevista de devolução é menor que a data atual e que ainda não foi enviado email de atraso
        ativo=True,
        data_prevista__lt=date.today(), #lt = menor que
        notificacao_atraso=False
    )
    

    for emprestimo in emprestimos_atrasados: # passa por cada emprestimo atrasado e envia email de aviso de atraso

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

        emprestimo.notificacao_atraso = True # marca que o email foi enviado e salva o emprestimo
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