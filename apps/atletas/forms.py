from django import forms
from apps.atletas.models import Atleta



class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['nome', 'data_nascimento', 'numero', 'encarregado', 'telefone', 'email', 'guarda_redes', 'ficha']