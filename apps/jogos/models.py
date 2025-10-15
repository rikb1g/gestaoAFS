from django.db import models



class Equipas(models.Model):
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Jogos(models.Model):
    jornada = models.IntegerField()
    visitado = models.ForeignKey(Equipas, on_delete=models.CASCADE, related_name='visitado')
    visitante = models.ForeignKey(Equipas, on_delete=models.CASCADE, related_name='adversario')
    data = models.DateField(default=None)
    golos_visitado= models.IntegerField(default=0)
    golos_visitante = models.IntegerField(default=0)
    titulares = models.ManyToManyField('atletas.Atleta', related_name='titulares', blank=True)
    suplentes = models.ManyToManyField('atletas.Atleta', related_name='suplentes', blank=True)
    capitao = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE, related_name='capitao')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nome


class EstatisticaJogo(models.Model):
    jogo = models.ForeignKey(Jogos, on_delete=models.CASCADE)
    atleta = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE)
    golos = models.IntegerField(default=0)
    assistencias = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

