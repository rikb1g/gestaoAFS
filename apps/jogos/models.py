from django.db import models

from apps.atletas.models import Atleta

class Equipas(models.Model):
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Jogos(models.Model):
    adversario = models.CharField(max_length=100)
    data = models.DateTimeField(null=True,blank=True)
    casa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class EquipaJogo(models.Model):
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Jogos, on_delete=models.CASCADE)
    capitao = models.BooleanField(default=False)
    titular = models.BooleanField(default=False)
    golos = models.IntegerField(default=0)
    assistencias = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.atleta} - {self.jogo}"
