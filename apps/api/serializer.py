from rest_framework import serializers
from apps.jogos.models import Jogos, EstatisticaJogo
from apps.atletas.models import Atleta


class JogosEstadoSeralizer(serializers.ModelSerializer):
    visitado = serializers.StringRelatedField()
    visitante = serializers.StringRelatedField()
    class Meta:
        model = Jogos
        fields = (
            'id',
            'inicio_jogo',
            'golos_visitado',
            'golos_visitante',
            'visitado',
            'visitante',
        )

class JogadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atleta
        fields = (
            'id',
            'nome',
        )


class JogadoresEmCampoSerializer(serializers.ModelSerializer):
    titulares = JogadorSerializer(many=True)
    suplentes = JogadorSerializer(many=True)
    capitao = JogadorSerializer(many=False)

    class Meta:
        model = Jogos
        fields = 'titulares', 'suplentes','capitao'

    
class EstatisticaJogoSerializer(serializers.ModelSerializer):
    atleta = JogadorSerializer(many=False)
    jogo = JogosEstadoSeralizer(many=False)

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


class SubstituicaoRequestSerializer(serializers.Serializer):
    jogo = serializers.IntegerField()
    atleta = serializers.IntegerField()
class SubstituicaoResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    status = serializers.CharField()
    total_minutos = serializers.FloatField(required=False)
    inicio = serializers.DateTimeField(required=False)

#serializer para marcar golos
#jogador
class JogadorGoloSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    golos = serializers.IntegerField()
    assistencias = serializers.IntegerField()

#jogo
class JogoGoloSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    golos_visitado = serializers.IntegerField()
    golos_visitante = serializers.IntegerField()


#serializer para marcar golos
class GoloResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    jogador = JogadorGoloSerializer()
    jogo = JogoGoloSerializer()


class GoloRequestSerializer(serializers.Serializer):
    atleta = serializers.IntegerField()
    jogo = serializers.IntegerField()


# golo equipa

class GoloEquipaRequestSerializer(serializers.Serializer):
    jogo = serializers.IntegerField()
    equipa = serializers.IntegerField()

class GoloEquipaResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    status = serializers.CharField()
    jogo = JogoGoloSerializer()


#iniciar jogos
class InicioJogoSerializer(serializers.Serializer):
    id= serializers.IntegerField()
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

class ListaJogosSerializer(serializers.Serializer):
    jogos = JogosEstadoSeralizer(many=True)
    class Meta:
        model = Jogos
        fields = (
            'id',
            'visitado',
            'visitante',
            'golos_visitado',
            'golos_visitante',
            'jornada',
            'data',
        )

