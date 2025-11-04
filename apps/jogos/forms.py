from django import forms
from apps.jogos.models import Jogos, EstatisticaJogo, Equipas


class JogosForm(forms.ModelForm):
    class Meta:
        model = Jogos
        fields = 'jornada', 'visitado', 'visitante', 'data', 'golos_visitado', 'golos_visitante', 'capitao','titulares', 'suplentes'
        widgets = {
            'jornada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jornada'}),
            'visitado': forms.Select(attrs={'class': 'form-control'}),
            'visitante': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Data do jogo', 'type': 'date'}),
            'golos_visitado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Golos visitado'}),
            'golos_visitante': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Golos visitante'}),
            'capitao': forms.Select(attrs={'class': 'form-control'}),
        }


class EstatisticaJogoForm(forms.ModelForm):
    class Meta:
        model = EstatisticaJogo
        fields = '__all__'
        widgets = {
            'jogo': forms.Select(attrs={'class': 'form-control'}),
            'atleta': forms.Select(attrs={'class': 'form-control'}),
            'golos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Golos'}),
            'assistencias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Assistencias'}),
        }

class EquipasForm(forms.ModelForm):
    class Meta:
        model = Equipas
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

