from django.db import models
from apps.atletas.models import Atleta


class Tamanho(models.Model):
    tamanho = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tamanho



class Equipamentos(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





    def __str__(self):
        return self.nome

class Encomenda(models.Model):
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE, null=True, blank=True)
    data_pedido = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Encomenda de {self.atleta} em {self.tamanho}"

class EncomendaItem(models.Model):
    encomenda = models.ForeignKey(Encomenda, on_delete=models.CASCADE,blank=True)
    equipamento = models.ForeignKey(Equipamentos, on_delete=models.PROTECT)
    entregue = models.BooleanField(default=False)
    data_entrega = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Encomenda de {self.encomenda.atleta} para {self.equipamento}"


def encomenda_kit(atleta, tamanho):
    encomendas_criadas = []
    todos_equipamentos = Equipamentos.objects.all()
    for equipamento in todos_equipamentos:
        if equipamento.nome == "jogo principal" and not atleta.guarda_redes:
            encomenda = Encomenda.objects.create(
                atleta=atleta,
                tamanho = tamanho)
            EncomendaItem.objects.create(
                encomenda=encomenda,
                equipamento=equipamento,
                entregue=False)
            encomendas_criadas.append(encomenda)
        elif equipamento.nome == 'guarda-redes azul' and atleta.guarda_redes:
            encomenda = Encomenda.objects.create(
                atleta=atleta,
                tamanho=tamanho)
            EncomendaItem.objects.create(
                encomenda=encomenda,
                equipamento=equipamento,
                entregue=False)
        elif equipamento.nome == 'fato de treino':
            encomenda = Encomenda.objects.create(
                atleta=atleta,
                tamanho=tamanho)
            EncomendaItem.objects.create(
                encomenda=encomenda,
                equipamento=equipamento,
                entregue=False)
        elif equipamento.nome == 'kit treino jogador':
            encomenda = Encomenda.objects.create(
                atleta=atleta,
                tamanho=tamanho)
            EncomendaItem.objects.create(
                encomenda=encomenda,
                equipamento=equipamento,
                entregue=False)
        elif equipamento.nome == 'polo de saída':
            encomenda = Encomenda.objects.create(
                atleta=atleta,
                tamanho=tamanho)
            EncomendaItem.objects.create(
                encomenda=encomenda,
                equipamento=equipamento,
                entregue=False)
        elif equipamento.nome == 'mochila':
            encomenda = Encomenda.objects.create(
                atleta=atleta,
                tamanho=tamanho)
            EncomendaItem.objects.create(
                encomenda=encomenda,
                equipamento=equipamento,
                entregue=False)
