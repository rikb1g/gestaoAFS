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

class EncomendaEquipamentos(models.Model):
    atleta = models.ForeignKey(Atleta,on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamentos,on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE, null=True, blank=True)
    entregue = models.BooleanField(default=False)
    data_entrega = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def encomenda_kit(self,atleta,tamanho):
        encomendas_criadas = []
        todos_equipamentos = Equipamentos.objects.all()
        for equipamento in todos_equipamentos:
            if equipamento.nome == "jogo principal" and not atleta.guarda_redes:
                encomenda = EncomendaEquipamentos.objects.create(
                    atleta=atleta,
                    equipamento=equipamento,
                    entregue=False,
                    tamanho = tamanho,
                    data_entrega=None,)
                encomendas_criadas.append(encomenda)

            elif equipamento.nome == 'guarda-redes azul' and atleta.guarda_redes:
                encomenda =EncomendaEquipamentos.objects.create(
                    atleta=atleta,
                    equipamento=equipamento,
                    entregue=False,
                    tamanho = tamanho,
                    data_entrega=None,)
                encomendas_criadas.append(encomenda)
            elif equipamento.nome == 'fato de treino':
                encomenda = EncomendaEquipamentos.objects.create(
                    atleta=atleta,
                    equipamento=equipamento,
                    entregue=False,
                    tamanho = tamanho,
                    data_entrega=None,)
                encomendas_criadas.append(encomenda)
            elif equipamento.nome == 'kit treino jogador' and not atleta.guarda_redes:
                encomenda = EncomendaEquipamentos.objects.create(
                    atleta=atleta,
                    equipamento=equipamento,
                    entregue=False,
                    tamanho = tamanho,
                    data_entrega=None,)
                encomendas_criadas.append(encomenda)
            elif equipamento.nome == 'kit treino guarda-redes' and atleta.guarda_redes:
                encomenda = EncomendaEquipamentos.objects.create(
                    atleta=atleta,
                    equipamento=equipamento,
                    entregue=False,
                    tamanho = tamanho,
                    data_entrega=None,)
                encomendas_criadas.append(encomenda)
            elif equipamento.nome == 'polo de saída':
                encomenda = EncomendaEquipamentos.objects.create(
                    atleta=atleta,
                    equipamento=equipamento,
                    entregue=False,
                    tamanho = tamanho,
                    data_entrega=None,)
                encomendas_criadas.append(encomenda)
            elif equipamento.nome == 'mochila':
                encomenda = EncomendaEquipamentos.objects.create(
                    atleta=atleta,
                    equipamento=equipamento,
                    entregue=False,
                    tamanho = tamanho,
                    data_entrega=None,)
                encomendas_criadas.append(encomenda)
        return encomendas_criadas
    def encomendar_artigos(self,atleta,tamanho,equipamento):
        encomenda = EncomendaEquipamentos.objects.create(
            atleta=atleta,
            equipamento=equipamento,
            entregue=False,
            tamanho = tamanho,
            data_entrega=None,)
        return encomenda

    def encomenda_entregue(self,id_encomenda):
        encomenda = EncomendaEquipamentos.objects.get(pk=id_encomenda)
        encomenda.entregue = True
        return encomenda






    def __str__(self):
        return f"Encomenda para {self.Atleta}"

