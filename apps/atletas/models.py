from django.db import models
from apps.jogos.models import Equipas



class Atleta(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    numero = models.IntegerField()
    encarregado = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    guarda_redes = models.BooleanField(default=False)
    ficha = models.FileField(upload_to='fichas/', null=True, blank=True)
    nome_camisola = models.CharField(max_length=100, null=True, blank=True)
    equipa = models.ForeignKey(Equipas, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nome
