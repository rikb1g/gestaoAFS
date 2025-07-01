import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AFS.settings')
import django
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from apps.atletas.models import Atleta
from apps.equipamentos.models import Equipamentos, Tamanho, EncomendaEquipamentos


class EquipamentosTest(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.atleta = Atleta.objects.create(
            nome='Manuel Sousa',
            data_nascimento='1999-01-01',
            numero=13,
            encarregado='Ricardo Sousa',
            telefone='123456789',
            email='YH6Q0@example.com',
            guarda_redes=True
        )
        self.tamanho = Tamanho.objects.create(
            tamanho='5-6')


        nomes_equipamentos = [
            "jogo principal", "fato de treino", "kit treino jogador",
            "polo de saída", "mochila", "kit treino guarda-redes",
            "guarda-redes azul"]
        self.equipamentos = []
        for nome in nomes_equipamentos:
            eq = Equipamentos.objects.filter(nome=nome).first()
            self.equipamentos.append(eq)


    def test_encomenda_kit_jogador(self):
        encomenda_isntance = EncomendaEquipamentos()
        not_redes = Atleta.objects.create(
            nome='Manuel Sousa',
            data_nascimento='1999-01-01',
            numero=13,
            encarregado='Ricardo Sousa',
            telefone='123456789',
            email='YH6Q0@example.com',
            guarda_redes=False
        )



        encomendas = encomenda_isntance.encomenda_kit(not_redes, self.tamanho)
        nomes_esperados = ["jogo principal", "fato de treino", "kit treino jogador", "polo de saída", "mochila"]
        self.assertEqual(len(encomendas), len(nomes_esperados))
        for encomenda in encomendas:
            self.assertEqual(encomenda.atleta, not_redes)
            self.assertEqual(encomenda.tamanho, self.tamanho)
            self.assertFalse(encomenda.entregue)
            self.assertIn(encomenda.equipamento.nome, nomes_esperados)

    def test_encomenda_kit_guarda_redes(self):
        encomenda_isntance = EncomendaEquipamentos()
        encomendas = encomenda_isntance.encomenda_kit(self.atleta, self.tamanho)
        nomes_esperados = ["guarda-redes azul", "fato de treino", "kit treino guarda-redes", "polo de saída", "mochila"]
        self.assertEqual(len(encomendas), len(nomes_esperados))
        for encomenda in encomendas:
            self.assertEqual(encomenda.atleta, self.atleta)
            self.assertEqual(encomenda.tamanho, self.tamanho)
            self.assertFalse(encomenda.entregue)
            self.assertIn(encomenda.equipamento.nome, nomes_esperados)


    def test_encomenda_entregue(self):
        equipamento = Equipamentos.objects.get_or_create(nome="jogo principal")[0]
        encomenda = EncomendaEquipamentos.objects.create(atleta=self.atleta, equipamento=equipamento, entregue=False)
        encomenda_entregue = EncomendaEquipamentos.encomenda_entregue(encomenda, encomenda.id)
        self.assertTrue(encomenda_entregue.entregue)




