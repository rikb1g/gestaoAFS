from django import forms
from .models import Equipamentos, Tamanho, EncomendaEquipamentos


class TamanhoForm(forms.ModelForm):
    class Meta:
        model = Tamanho
        fields = ['tamanho']




class EquipamentosForm(forms.ModelForm):
    class Meta:
        model = Equipamentos
        fields = ['nome', 'descricao']



class EncomendaEquipamentosForm(forms.ModelForm):
    class Meta:
        model = EncomendaEquipamentos
        fields = ['atleta', 'equipamento', 'tamanho']