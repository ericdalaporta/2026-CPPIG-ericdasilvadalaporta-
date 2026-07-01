from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Emprestimo, ItemEmprestimo
from chaves.models import CopiaChave


class EmprestimoModelForm(forms.ModelForm):
    copias = forms.ModelMultipleChoiceField( # pode selecionar varias copias
        queryset=CopiaChave.objects.filter(status='DISPONIVEL'), # mostra só as cópias disponíveis
        required=False,
        label='Cópias de Chave'
    )
    
    class Meta:
        model = Emprestimo # diz que esse form é baseado no model Emprestimo
        #daí cria os campos do form com base nos campos do model

        fields = [
            'cliente',
            'data_retirada',
            'data_prevista',
        ]

        widgets = {
            'data_retirada': forms.DateInput(attrs={'type': 'date'}),
            'data_prevista': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # o init serve pra caso criar emprestimo = mostra copias disponiveis
        # e pra caso estiver editando, mostra as disponiveis + as que já estão vinculadas ao emprestimo
       
        if self.instance.pk: # se o emprestimo ja existe, mostra as copias disponiveis + as que já estão vinculadas ao emprestimo
        # se lê como "se esse empréstimo já tem ID, ele existe e tá sendo editado"
        
            copias_vinculadas = self.instance.itens.values_list(
                'copia_chave_id',
                flat=True
            )
            # pegue os itens desse emprestimos e guarde os id das copias vinculadas, pra poder pré-selecionar no form e mostrar no queryset

            self.fields['copias'].queryset = CopiaChave.objects.filter(
                Q(status='DISPONIVEL') |
                Q(id__in=copias_vinculadas)
            ).distinct() # define quais copias vao aparecer no form de acordo com o filtro
            # o filtro mostra disponiveis ou as que ja tao vinculadas ao emprestimo


        else:
            # Novo: mostrar só disponível
            self.fields['copias'].queryset = CopiaChave.objects.filter(
                status='DISPONIVEL'
            )
    
class ItemEmprestimoModelForm(forms.ModelForm):
    # itemEmprestimo é a relação entre emprestimo e copia de chave, então esse form serve pra editar o status do item emprestimo, que é o status da copia de chave vinculada ao emprestimo
    # ou seja, é a tabela intermediária entre emprestimo e copia de chave, que tem o status da copia de chave vinculada ao emprestimo
    # O ItemEmprestimo também guarda informações extras, como status, multa e data de devolução.
    class Meta:
        model = ItemEmprestimo
        fields = ['copia_chave', 'status']