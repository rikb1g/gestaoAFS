import sys
import os
from django.test import Client, TestCase

from apps.atletas.models import Atleta
from apps.jogos.models import Equipas, EquipaJogo,Jogos
from django.utils import timezone
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AFS.settings')
import django
django.setup()

from django.test import TestCase

class JogosTest(TestCase):
    def _setUp(self):
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
        self.adversario= Equipas.objects.create(
            nome='FCP'
        )
        self.jogo = EquipaJogo.objects.create(
            adversario='jogo principal',
            atleta=self.atleta
        )

    def test_criar_jogo(self):
        jogo = EquipaJogo.objects.create(
            adversario=self.adversario,
            data = timezone.now(),
            casa = True,

        )
        self.assertEqual(jogo.adversario, self.adversario)

    def test_jodador_jogo(self):
        jogador = EquipaJogo.objects.create(
            atleta=self.atleta,
            jogo = self.jogo,
            titular = True,
            capitao = True,
            golos =1,
            assistencias = 0

        )
        self.assertEqual(jogador.atleta, self.atleta)
        self.assertEqual(jogador.jogo, self.jogo)
        self.assertEqual(jogador.titular, True)
        self.assertEqual(jogador.capitao, True)
        self.assertEqual(jogador.golos, 1)
        self.assertEqual(jogador.assistencias, 0)