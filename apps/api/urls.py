from django.urls import path
from apps.api import views

app_name = 'api'

urlpatterns = [
    path('jogos/<int:jogo_id>/', views.estado_jogo, name='estado_jogos'),
    path('estatistica_jogo/<int:jogo_id>/', views.estatisticas_jogo, name='estatistica_jogo'),
    path('jogadores_em_campo/<int:jogo_id>/', views.jogadores_em_campo, name='jogadores_em_campo'),
    path('subsituicao_jogo/', views.substituicao_jogo, name='api_substituicao_jogo'),
    path('marcar_golo_atleta/', views.marcar_golo, name='api_marcar_golo'),
    path('golo_equipa/', views.golo_equipa, name='api_golo_equipa'),
    path('iniciar_jogo/', views.iniciar_jogo, name='api_intervalo_jogo'),
    path('intervalo_jogo/', views.intervalo_jogo, name='api_intervalo_jogo'),
    path('finalizar_jogo/', views.finalizar_jogo, name='api_finalizar_jogo'),
    path('lista_jogos/', views.lista_jogos, name='api_lista_jogos'),

]