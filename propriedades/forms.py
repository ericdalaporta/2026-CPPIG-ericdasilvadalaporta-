from django import forms
from django.db.models import Q
from .models import Propriedade, Portao

class PropriedadeModelForm(forms.ModelForm):
    propriedade_linkada = forms.ModelChoiceField(
        queryset=Propriedade.objects.filter(~Q(tipo='PORTAO')),
        required=False,
        label='Propriedade Linkada',
        empty_label='Nenhuma'
    )
    
    class Meta:
        model = Propriedade
        fields = ['nome', 'tipo', 'portao_associado']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo'}),
            'portao_associado': forms.Select(attrs={'class': 'form-select', 'id': 'id_portao_associado'}),
        }
        error_messages = {
            'nome': {'required': 'O Nome da propriedade é obrigatório'},
            'tipo': {'required': 'O Tipo é obrigatório'},
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['portao_associado'].queryset = Portao.objects.all()
        self.fields['portao_associado'].required = False
        self.fields['portao_associado'].empty_label = '-- Selecione um portão --'
        
        # se to editando um Portão, mostra o campo propriedade_linkada
        if self.instance.pk and self.instance.tipo == 'PORTAO':
            portao_instance = Portao.objects.filter(pk=self.instance.pk).first()
            if portao_instance and portao_instance.propriedade_linkada:
                self.fields['propriedade_linkada'].initial = portao_instance.propriedade_linkada
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # if Portão, salvar propriedade_linkada
        if instance.tipo == 'PORTAO':
            portao = Portao.objects.filter(pk=instance.pk).first()
            if portao:
                portao.propriedade_linkada = self.cleaned_data.get('propriedade_linkada')
                portao.save()
        
        if commit:
            instance.save()
        return instance

