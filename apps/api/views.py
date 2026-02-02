from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone


from apps.jogos.models import Jogos, EstatisticaJogo, HistoricoSubstituição
from apps.atletas.models import Atleta, Equipas
from apps.api import serializer

@api_view(['GET'])
def estado_jogo(request, jogo_id):
    jogo = get_object_or_404(Jogos, id=jogo_id)
    serializer_data = serializer.JogosEstadoSerializer(jogo)
    return Response(serializer_data.data)


@api_view(['GET'])
def jogadores_em_campo(request, jogo_id):
    jogo = get_object_or_404(Jogos, id=jogo_id)
    serializer_data = serializer.JogadoresEmCampoSerializer(jogo)
    return Response(serializer_data.data)


@api_view(['GET'])
def estatisticas_jogo(request, jogo_id):
    estatisticas = EstatisticaJogo.objects.filter(jogo__id=jogo_id)
    serializer_data = serializer.EstatisticaJogoSerializer(estatisticas, many=True)
    return Response(serializer_data.data)

@api_view(['POST'])
def substituicao_jogo(request):
    # Valida o request
    serializer_ = serializer.SubstituicaoRequestSerializer(data=request.data)
    serializer_.is_valid(raise_exception=True)

    jogo_id = serializer_.validated_data['jogo']
    atleta_id = serializer_.validated_data['atleta']

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

            return Response(serializer.SubstituicaoResponseSerializer({
                "success": True,
                "status": "saiu",
                "total_minutos": estatistica.total_minutos
            }).data)
        else:
            estatistica.em_campo = False
            estatistica.save()
            return Response(serializer.SubstituicaoResponseSerializer({
                "success": True,
                "status": "saiu (jogo em pausa)"
            }).data)
    else:
        # Jogador entra
        if not jogo.pausa:
            estatistica.inicio = timezone.now()
            estatistica.em_campo = True
            estatistica.save()
            return Response(serializer.SubstituicaoResponseSerializer({
                "success": True,
                "status": "entrou",
                "total_minutos": estatistica.total_minutos,
                "inicio": estatistica.inicio,
            }).data)
        else:
            estatistica.em_campo = True
            estatistica.save()
            return Response(serializer.SubstituicaoResponseSerializer({
                "success": True,
                "status": "entrou (jogo em pausa)",
                'total_minutos': estatistica.total_minutos,
                'inicio': estatistica.inicio,
            }).data)
        
@api_view(['POST'])
def marcar_golo(request):
    """
    Marca um golo para um atleta e atualiza o placar do jogo.
    Retorna JSON com os dados do jogador e do jogo atualizados.
    """
    # Valida o request
    golo_request = serializer.GoloRequestSerializer(data=request.data)
    golo_request.is_valid(raise_exception=True)

    jogo_id = golo_request.validated_data['jogo']
    atleta_id = golo_request.validated_data['atleta']

    # Busca objetos no DB
    jogo = get_object_or_404(Jogos, pk=jogo_id)
    atleta = get_object_or_404(Atleta, pk=atleta_id)
    estatisticas = get_object_or_404(EstatisticaJogo, atleta=atleta, jogo=jogo)

    # Atualiza estatísticas do jogador
    estatisticas.golos += 1
    estatisticas.save()

    # Atualiza o placar do jogo
    if atleta.equipa == jogo.visitado:
        jogo.golos_visitado += 1
    else:
        jogo.golos_visitante += 1
    jogo.save()

    # Prepara os dados para o serializer de resposta
    response_data = {
        "success": True,
        "message": "Golo marcado com sucesso!",
        "jogador": {
            "id": atleta.id,
            "golos": estatisticas.golos,
            "assistencias": estatisticas.assistencias
        },
        "jogo": {
            "id": jogo.id,
            "golos_visitado": jogo.golos_visitado,
            "golos_visitante": jogo.golos_visitante
        }
    }

    # Serializa e retorna
    response_serializer = serializer.GoloResponseSerializer(response_data)
    return Response(response_serializer.data)

@api_view(['POST'])
def anular_golo_jogador(request):
    s = serializer.GoloRequestSerializer(data=request.data)
    s.is_valid(raise_exception=True)

    jogo = get_object_or_404(Jogos, pk=s.validated_data['jogo'])
    atleta = get_object_or_404(Atleta, pk=s.validated_data['atleta'])
    estatisticas = get_object_or_404(EstatisticaJogo, atleta=atleta, jogo=jogo)

    estatisticas.golos = max(estatisticas.golos - 1, 0)
    estatisticas.save()

    if atleta.equipa == jogo.visitado:
        jogo.golos_visitado = max(jogo.golos_visitado - 1, 0)
    else:
        jogo.golos_visitante = max(jogo.golos_visitante - 1, 0)
    jogo.save()

    return Response(serializer.GoloResponseSerializer({
        "success": True,
        "message": "Golo anulado com sucesso!",
        "jogador": {
            "id": atleta.id,
            "golos": estatisticas.golos,
            "assistencias": estatisticas.assistencias
        },
        "jogo": {
            "id": jogo.id,
            "golos_visitado": jogo.golos_visitado,
            "golos_visitante": jogo.golos_visitante
        }
    }).data)


# -----------------------------
# Golos da equipa
# -----------------------------
@api_view(['POST'])
def golo_equipa(request):
    s = serializer.GoloEquipaRequestSerializer(data=request.data)
    s.is_valid(raise_exception=True)

    jogo = get_object_or_404(Jogos, pk=s.validated_data['jogo'])
    equipa_id = s.validated_data['equipa']

    if equipa_id == jogo.visitado.id:
        jogo.golos_visitado += 1
    elif equipa_id == jogo.visitante.id:
        jogo.golos_visitante += 1
    else:
        return Response(serializer.GoloEquipaResponseSerializer({
            "success": False,
            "status": "Equipa inválida",
            "jogo": {
                "id": jogo.id,
                "golos_visitado": jogo.golos_visitado,
                "golos_visitante": jogo.golos_visitante
            }
        }).data)

    jogo.save()
    return Response(serializer.GoloEquipaResponseSerializer({
        "success": True,
        "status": "Golo marcado com sucesso!",
        "jogo": {
            "id": jogo.id,
            "golos_visitado": jogo.golos_visitado,
            "golos_visitante": jogo.golos_visitante
        }
    }).data)


# -----------------------------
# Assistências
# -----------------------------
@api_view(['POST'])
def atribuir_assistencia(request):
    s = serializer.GoloRequestSerializer(data=request.data)
    s.is_valid(raise_exception=True)

    jogo = get_object_or_404(Jogos, pk=s.validated_data['jogo'])
    atleta = get_object_or_404(Atleta, pk=s.validated_data['atleta'])
    estatisticas = get_object_or_404(EstatisticaJogo, atleta=atleta, jogo=jogo)

    estatisticas.assistencias += 1
    estatisticas.save()

    return Response(serializer.GoloResponseSerializer({
        "success": True,
        "message": "Assistência atribuída com sucesso!",
        "jogador": {
            "id": atleta.id,
            "golos": estatisticas.golos,
            "assistencias": estatisticas.assistencias
        }
    }).data)


@api_view(['POST'])
def anular_assistencia(request):
    s = serializer.GoloRequestSerializer(data=request.data)
    s.is_valid(raise_exception=True)

    jogo = get_object_or_404(Jogos, pk=s.validated_data['jogo'])
    atleta = get_object_or_404(Atleta, pk=s.validated_data['atleta'])
    estatisticas = get_object_or_404(EstatisticaJogo, atleta=atleta, jogo=jogo)

    estatisticas.assistencias = max(estatisticas.assistencias - 1, 0)
    estatisticas.save()

    return Response(serializer.GoloResponseSerializer({
        "success": True,
        "message": "Assistência anulada com sucesso!",
        "jogador": {
            "id": atleta.id,
            "golos": estatisticas.golos,
            "assistencias": estatisticas.assistencias
        }
    }).data)
@api_view(['POST'])
def iniciar_jogo(request):
    serializer_ = serializer.IniciarJogoRequestSerializer(data=request.data)
    serializer_.is_valid(raise_exception=True)

    jogo_id = serializer_.validated_data['jogo']
    atletas_ids = serializer_.validated_data['atletas']

    jogo = get_object_or_404(Jogos, pk=jogo_id)
    jogo.inicio_jogo = timezone.now()
    jogo.pausa = False
    jogo.save()
    for atleta_id in atletas_ids:
        estatisticas = EstatisticaJogo.objects.get(atleta_id=atleta_id, jogo=jogo)
        estatisticas.inicio = timezone.now()
        estatisticas.em_campo = True
        estatisticas.save()

    return Response(serializer.IniciarJogoResponseSerializer({
        "success": True,
        "message": "Jogo iniciado com sucesso!",
        'jogo': {
            'id': jogo.id,
            'visitado': jogo.visitado,
            'visitante': jogo.visitante,
            'inicio': jogo.inicio_jogo.isoformat() if jogo.inicio_jogo else None,
        }
    }).data)

@api_view(['POST'])
def intervalo_jogo(request):
    serializer_data = serializer.IniciarJogoRequestSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)

    jogo_id = serializer_data.validated_data['jogo']
    atletas_ids = serializer_data.validated_data['atletas']
    jogo = get_object_or_404(Jogos, pk=jogo_id)
    jogo.pausa = True
    jogo.save()
    atletas_response = []

    for atleta_id in atletas_ids:
        atleta_estatistica = EstatisticaJogo.objects.get(atleta__id=atleta_id, jogo=jogo)
        atleta_estatistica.fim = timezone.now()
        atleta_estatistica.em_campo = False
        atleta_estatistica.save()
        if atleta_estatistica.inicio:
            total_minutos = (atleta_estatistica.fim - atleta_estatistica.inicio).total_seconds() / 60
            atleta_estatistica.total_minutos += total_minutos

        HistoricoSubstituição.objects.create(jogo=jogo, atleta=atleta_estatistica.atleta,
                                                 entrou=atleta_estatistica.inicio, saiu=atleta_estatistica.fim,
                                                 total_minutos=atleta_estatistica.total_minutos)
        atleta_estatistica.inicio = None
        atleta_estatistica.fim = None
        atleta_estatistica.save()

    atletas_response.append({
        'id': atleta_estatistica.atleta.id,
        'nome': atleta_estatistica.atleta.nome,
        'inicio': atleta_estatistica.inicio.isoformat() if atleta_estatistica.inicio else None,
        'total_minutos': atleta_estatistica.total_minutos,
        'golos': atleta_estatistica.golos,
        "assistencias": atleta_estatistica.assistencias,
    })
    
    

    return Response(serializer.IniciarJogoResponseSerializer({
        "success": True,
        "message": "Jogo iniciado com sucesso!",
        'jogo': {
            'id': jogo.id,
            'visitado': jogo.visitado,
            'visitante': jogo.visitante,
            'inicio': jogo.inicio_jogo.isoformat() if jogo.inicio_jogo else None,
        },
        'atletas': atletas_response,
    }).data)
    


@api_view(['POST'])
def finalizar_jogo(request):
    serializer_data = serializer.IniciarJogoRequestSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)

    jogo_id = serializer_data.validated_data['jogo']
    atletas_id = serializer_data.validated_data['atletas']
    jogo = get_object_or_404(Jogos, pk=jogo_id)
    jogo.pausa = False
    jogo.save()
    atletas_response = []

    for atleta_id in atletas_id:
        atleta_estatistica = EstatisticaJogo.objects.get(atleta__id=atleta_id, jogo=jogo)
        atleta_estatistica.fim = timezone.now()
        atleta_estatistica.em_campo = False
        atleta_estatistica.save()
        if atleta_estatistica.inicio:
            total_minutos = (atleta_estatistica.fim - atleta_estatistica.inicio).total_seconds() / 60
            atleta_estatistica.total_minutos += total_minutos

        HistoricoSubstituição.objects.create(jogo=jogo, atleta=atleta_estatistica.atleta,
                                                 entrou=atleta_estatistica.inicio, saiu=atleta_estatistica.fim,
                                                 total_minutos=atleta_estatistica.total_minutos)
        atleta_estatistica.inicio = None
        atleta_estatistica.fim = None
        atleta_estatistica.save()

    atletas_response.append({
        'id': atleta_estatistica.atleta.id,
        'nome': atleta_estatistica.atleta.nome,
        'total_minutos': atleta_estatistica.total_minutos,
        'golos': atleta_estatistica.golos,
        'assistencias': atleta_estatistica.assists,
    })


    return Response(serializer.IniciarJogoResponseSerializer({
        "success": True,
        "message": "Jogo iniciado com sucesso!",
        'jogo': {
            'id': jogo.id,
            'visitado': jogo.visitado,
            'visitante': jogo.visitante,
            'inicio': jogo.inicio_jogo.isoformat() if jogo.inicio_jogo else None,
        },
        'atletas': atletas_response,
    }).data)


@api_view(['GET'])
def lista_jogos(request):
    jogo = Jogos.objects.all()
    serializer_data = serializer.ListaJogosSerializer(jogo, many=True)
    return Response(serializer_data.data)
