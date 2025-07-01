from django.db import models





class Jogos(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    hora = models.TimeField()
    local = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class EquipaJogo(models.Model):
    jogo = models.ForeignKey(Jogos, on_delete=models.CASCADE)
    capitao = models.BooleanField(default=False)
    titular = models.BooleanField(default=False)
    suplente = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.atleta} - {self.jogo}"
