from apps.equipamentos.models import Tamanho, Equipamentos



from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.equipamentos.models import Tamanho

@receiver(post_migrate)
def criar_tamanhos(sender, **kwargs):
    tamanhos = ['5-6', '6-7', '7-8', '8-9', '9-10']
    for t in tamanhos:
        Tamanho.objects.get_or_create(tamanho=t)

@receiver(post_migrate)
def criar_equipamentos_iniciais(sender, **kwargs):
    equipamentos_iniciais = [
        ("jogo principal", "equipamento jogo principal"),
        ("jogo alternativo", "equipamento jogo secundario"),
        ("guarda-redes azul", "equipamento guarda-redes azul"),
        ("guarda-redes amarelo", "equipamento guarda-redes amarelo"),
        ("fato de treino", "fato de treino adidas atletas"),
        ("kit treino jogador", "kit de treino vermelho (tshirt, calção e meias)"),
        ("kit treino guarda-redes", "kit de treino preto (tshirt, calção e meias)"),
        ("polo de saída", "polo de saída"),
        ("mochila", "mochila"),
        ("Kispo", "Blusão/kispo"),
        ("calcão", "calcão"),
        ("meias", "meias de jogo"),
        ("Kit Completo", "Kit completo"),
    ]

    for nome, descricao in equipamentos_iniciais:
        Equipamentos.objects.get_or_create(nome=nome, defaults={"descricao": descricao})