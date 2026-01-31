from rest_framework import serializers
from .models import Jogos, Atleta, EstatisticaJogo

# =========================
# Serializers de Jogos
# =========================
class JogosEstadoSerializer(serializers.ModelSerializer):
    visitado = serializers.StringRelatedField()
    visitante = serializers.StringRelatedField()
    visitado_id = serializers.IntegerField(source='visitado.id', read_only=True)
    visitante_id = serializers.IntegerField(source='visitante.id', read_only=True)

    class Meta:
        model = Jogos
        fields = (
            'id',
            'inicio_jogo',
            'golos_visitado',
            'golos_visitante',
            'visitado',
            'visitante',
            'visitado_id',
            'visitante_id',
        )

# =========================
# Serializers de Atletas
# =========================
class JogadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atleta
        fields = ('id', 'nome')

class JogadoresEmCampoSerializer(serializers.ModelSerializer):
    titulares = JogadorSerializer(many=True)
    suplentes = JogadorSerializer(many=True)
    capitao = JogadorSerializer()

    class Meta:
        model = Jogos
        fields = ('titulares', 'suplentes', 'capitao')

# =========================
# Serializers de Estatísticas
# =========================
class EstatisticaJogoSerializer(serializers.ModelSerializer):
    atleta = JogadorSerializer()
    jogo = JogosEstadoSerializer()

    class Meta:
        model = EstatisticaJogo
        fields = (
            'jogo', 
            'atleta', 
            'golos', 
            'assistencias', 
            'inicio', 
            'fim',
            'total_minutos',
            'em_campo',
        )

# =========================
# Substituição
# =========================
class SubstituicaoRequestSerializer(serializers.Serializer):
    jogo = serializers.IntegerField()
    atleta = serializers.IntegerField()

class SubstituicaoResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    status = serializers.CharField()
    total_minutos = serializers.FloatField(required=False)
    inicio = serializers.DateTimeField(required=False)

# =========================
# Marcar Golos
# =========================
class JogadorGoloSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    golos = serializers.IntegerField()
    assistencias = serializers.IntegerField()

class JogoGoloSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    golos_visitado = serializers.IntegerField()
    golos_visitante = serializers.IntegerField()

class GoloResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    jogador = JogadorGoloSerializer()
    jogo = JogoGoloSerializer()

class GoloRequestSerializer(serializers.Serializer):
    atleta = serializers.IntegerField()
    jogo = serializers.IntegerField()

# =========================
# Golo por Equipa
# =========================
class GoloEquipaRequestSerializer(serializers.Serializer):
    jogo = serializers.IntegerField()
    equipa = serializers.IntegerField()

class GoloEquipaResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    status = serializers.CharField()
    jogo = JogoGoloSerializer()

# =========================
# Iniciar Jogo
# =========================
class InicioJogoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    visitado = serializers.StringRelatedField()
    visitante = serializers.StringRelatedField()
    inicio = serializers.DateTimeField()

class IniciarJogoRequestSerializer(serializers.Serializer):
    jogo = serializers.IntegerField()
    atletas = serializers.ListField(child=serializers.IntegerField())

class IniciarJogoResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    status = serializers.CharField()
    jogo = InicioJogoSerializer()

# =========================
# Lista de Jogos
# =========================
class ListaJogosSerializer(serializers.Serializer):
    jogos = JogosEstadoSerializer(many=True)
