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


class AtletasTest(TestCase):
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


    def test_criar_atleta(self):
        novo = Atleta.objects.create(
            nome='Manuel Sousa',
            data_nascimento='1999-01-01',
            numero=13,
            encarregado='Ricardo Sousa',
            telefone='123456789',
            email='YH6Q0@example.com',
            guarda_redes=True
        )
        self.assertEqual(novo.nome, 'Manuel Sousa')
        self.assertEqual(str(novo.data_nascimento), '1999-01-01')
        self.assertEqual(novo.numero, 13)
        self.assertEqual(novo.encarregado, 'Ricardo Sousa')
        self.assertEqual(novo.telefone, '123456789')
        self.assertEqual(novo.email, 'YH6Q0@example.com')
        self.assertTrue(novo.guarda_redes)

    def test_delete_atleta(self):
        self.assertEqual(Atleta.objects.count(), 1)
        response = self.cliente.post(reverse('atletas:delete_atleta', args=[self.atleta.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Atleta.objects.count(), 0)



if __name__ == '__main__':
    import unittest
    unittest.main()
