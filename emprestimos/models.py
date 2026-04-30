from django.db import models
from datetime import date


class Emprestimo(models.Model):
    data_retirada = models.DateField('Data de Retirada', blank=False, help_text='Data da retirada do empréstimo')
    data_prevista = models.DateField('Data Prevista', blank=False, help_text='Data prevista de devolução')
    data_devolucao = models.DateField('Data de Devolução', null=True, blank=True, help_text='Data da devolução do empréstimo')
    multa = models.IntegerField('Multa', default=0, help_text='Multa por atraso')

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'

    def __str__(self):
        return f'Empréstimo {self.id}'
    
    def calcular_multa(self):
        """Calcula multa de 200 reais por dia de atraso se não foi devolvido"""
        if self.data_devolucao is None:
            dias_atraso = (date.today() - self.data_prevista).days
            if dias_atraso > 0:
                return dias_atraso * 200
        return 0
    
    def esta_atrasado(self):
        """Verifica se está atrasado"""
        return self.data_devolucao is None and date.today() > self.data_prevista
    
    def dias_atraso(self):
        """Retorna quantidade de dias em atraso"""
        if self.esta_atrasado():
            return (date.today() - self.data_prevista).days
        return 0
    
    def toggle_status(self):
        """Marca como devolvido ou volta a pendente"""
        if self.data_devolucao is None:
            self.data_devolucao = date.today()
        else:
            self.data_devolucao = None
        self.save()
    
    def get_status(self):
        """Retorna o status do empréstimo"""
        return 'Devolvida' if self.data_devolucao else 'Pendente'
