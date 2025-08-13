from django import forms
from apps.atletas.models import Atleta
from .models import Equipamentos, Tamanho, EncomendaItem, Encomenda


class TamanhoForm(forms.ModelForm):
    class Meta:
        model = Tamanho
        fields = ['tamanho']

        widgets = {
            'tamanho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tamanho do equipamento'}),
        }




class EquipamentosForm(forms.ModelForm):
    class Meta:
        model = Equipamentos
        fields = ['nome', 'descricao']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do equipamento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do equipamento'}),
        }


class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['atleta', 'tamanho']

        widgets = {
            'atleta': forms.Select(attrs={'class': 'form-control'}),
            'tamanho': forms.Select(attrs={'class': 'form-control'}),
        }


class EncomendaItemForm(forms.ModelForm):
    class Meta:
        model = EncomendaItem
        fields = ['equipamento']

        widgets = {
            'equipamento': forms.Select(attrs={'class': 'form-control'}),
        }