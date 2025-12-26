from datetime import timedelta
from django.db import models
from django.urls import reverse




class Equipas(models.Model):
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('jogos:games_list', )


class Jogos(models.Model):
    jornada = models.IntegerField()
    visitado = models.ForeignKey(Equipas, on_delete=models.CASCADE, related_name='visitado')
    visitante = models.ForeignKey(Equipas, on_delete=models.CASCADE, related_name='adversario')
    data = models.DateField(default=None)
    golos_visitado= models.IntegerField(default=0)
    golos_visitante = models.IntegerField(default=0)
    inicio_jogo = models.DateTimeField(default=None,null=True,blank=True)
    pausa = models.BooleanField(default=True, null=True, blank=True)
    fim_jogo = models.DateTimeField(default=None,null=True,blank=True)
    titulares = models.ManyToManyField('atletas.Atleta', related_name='titulares', blank=True)
    suplentes = models.ManyToManyField('atletas.Atleta', related_name='suplentes', blank=True)
    capitao = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE, related_name='capitao')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.jornada} - {self.visitado} vs {self.visitante}" 


class EstatisticaJogo(models.Model):
    jogo = models.ForeignKey(Jogos, on_delete=models.CASCADE)
    atleta = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE)
    golos = models.IntegerField(default=0)
    inicio = models.DateTimeField(default=None, null=True, blank=True)
    fim = models.DateTimeField(default=None, null=True, blank=True)
    total_minutos = models.FloatField(default=0)
    assistencias = models.IntegerField(default=0)
    em_campo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tempo_formatado_total_minutos(self):
        if not self.total_minutos:  # cobre None e 0
            return "00:00"

        delta = timedelta(minutes=self.total_minutos)
        total_segundos = int(delta.total_seconds())
       
        minutos, segundos = divmod(total_segundos, 60)
        if minutos < 10 and segundos < 10:
            return f"0{minutos}:0{segundos}"
        else:
            return f"{minutos:02d}:{segundos:02d}"

    def __str__(self):
        return f"{self.atleta} - {self.jogo}"

class HistoricoSubstituição(models.Model):
    jogo = models.ForeignKey(Jogos, on_delete=models.CASCADE)
    atleta = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE)
    entrou = models.DateTimeField(default=None,null=True,blank=True)
    saiu = models.DateTimeField(default=None,null=True,blank=True)
    total_minutos = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.atleta} - {self.jogo}"
    