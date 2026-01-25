from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone


from apps.jogos.models import Jogos, EstatisticaJogo, HistoricoSubstituição
from apps.atletas.models import Atleta, Equipas
from apps.api.serializer import JogosEstadoSeralizer, JogadoresEmCampoSerializer, EstatisticaJogoSerializer, SubstituicaoRequestSerializer, SubstituicaoResponseSerializer
from apps.api.serializer import GoloRequestSerializer, GoloResponseSerializer, GoloEquipaRequestSerializer, GoloEquipaResponseSerializer


@api_view(['GET'])
def estado_jogo(request, jogo_id):
    jogo = get_object_or_404(Jogos, id=jogo_id)
    serializer = JogosEstadoSeralizer(jogo)
    return Response(serializer.data)


@api_view(['GET'])
def jogadores_em_campo(request, jogo_id):
    jogo = get_object_or_404(Jogos, id=jogo_id)
    serializer = JogadoresEmCampoSerializer(jogo)
    return Response(serializer.data)


@api_view(['GET'])
def estatisticas_jogo(request, jogo_id):
    estatisticas = EstatisticaJogo.objects.filter(jogo__id=jogo_id)
    serializer = EstatisticaJogoSerializer(estatisticas, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def substituicao_jogo(request):
    # Valida o request
    serializer = SubstituicaoRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    jogo_id = serializer.validated_data['jogo']
    atleta_id = serializer.validated_data['atleta']

    # Busca objetos
    jogo = get_object_or_404(Jogos, pk=jogo_id)
    estatistica = get_object_or_404(EstatisticaJogo, atleta__id=atleta_id, jogo=jogo)

    # Lógica de substituição
    if estatistica.em_campo:
        # Jogador sai
        if not jogo.pausa:
            estatistica.fim = timezone.now()
            estatistica.em_campo = False

            total_minutos = 0
            if estatistica.inicio:
                total_minutos = (estatistica.fim - estatistica.inicio).total_seconds() / 60
                estatistica.total_minutos += total_minutos

            # Cria histórico
            HistoricoSubstituição.objects.create(
                jogo=jogo,
                atleta=estatistica.atleta,
                entrou=estatistica.inicio,
                saiu=estatistica.fim,
                total_minutos=estatistica.total_minutos
            )

            # Reset dos tempos
            estatistica.inicio = None
            estatistica.fim = None
            estatistica.save()

            return Response(SubstituicaoResponseSerializer({
                "success": True,
                "status": "saiu",
                "total_minutos": estatistica.total_minutos
            }).data)
        else:
            estatistica.em_campo = False
            estatistica.save()
            return Response(SubstituicaoResponseSerializer({
                "success": True,
                "status": "saiu (jogo em pausa)"
            }).data)
    else:
        # Jogador entra
        if not jogo.pausa:
            estatistica.inicio = timezone.now()
            estatistica.em_campo = True
            estatistica.save()
            return Response(SubstituicaoResponseSerializer({
                "success": True,
                "status": "entrou"
            }).data)
        else:
            estatistica.em_campo = True
            estatistica.save()
            return Response(SubstituicaoResponseSerializer({
                "success": True,
                "status": "entrou (jogo em pausa)"
            }).data)
        
    
@api_view(['POST'])
def marcar_golo(request):
    serializer = GoloRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    jogo_id = serializer.validated_data['jogo']
    atleta_id = serializer.validated_data['atleta']

    #buscar os objetos
    jogo = get_object_or_404(Jogos, pk=jogo_id)
    atleta = get_object_or_404(Atleta, pk=atleta_id)
    
    estatisticas = EstatisticaJogo.objects.get(atleta=atleta, jogo=jogo)

    estatisticas.golos += 1
    estatisticas.save()

    if atleta.equipa == jogo.visitado:
        jogo.golos_visitado += 1
        jogo.save()
    else:
        jogo.golos_visitante += 1
        jogo.save()

    return Response(GoloResponseSerializer({
        "success": True,
        "message": "Golo marcado com sucesso!"
    }).data)

# golo equipa
@api_view(['POST'])
def golo_equipa(request):
    serializer = GoloEquipaRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    jogo_id = serializer.validated_data['jogo']
    equipa_id = serializer.validated_data['equipa']

    jogo = get_object_or_404(Jogos, pk=jogo_id)

    if equipa_id == jogo.visitado.id:
        jogo.golos_visitado += 1
    elif equipa_id == jogo.visitante.id:
        jogo.golos_visitante += 1
    else:
        return Response(GoloEquipaResponseSerializer({
            "success": False,
            "message": "Equipa inválida"
        }).data)

    jogo.save()

    return Response(GoloEquipaResponseSerializer({
        "success": True,
        "message": "Golo marcado com sucesso!"
    }).data)