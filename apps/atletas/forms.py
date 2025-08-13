from django import forms
from apps.atletas.models import Atleta



class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['nome', 'data_nascimento', 'numero', 'encarregado', 'telefone', 'email', 'guarda_redes', 'ficha']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do atleta'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Data de nascimento',                                       'type': 'date'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número do atleta'}),
            'encarregado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Encarregado do atleta'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone do atleta'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email do atleta'}),
            'guarda_redes': forms.CheckboxInput(attrs={'class': 'form-check-input', 'placeholder': 'Guarda redes do atleta'}),
            'ficha': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Ficha do atleta'}),
        }

    def __init__(self, *args, **kwargs):
        super(AtletaForm, self).__init__(*args, **kwargs)
        self.fields['ficha'].required = False


