from django.urls import path
from apps.jogos import views

app_name = 'jogos'

urlpatterns = [
    path('jogos', views.JogosListView.as_view(), name='games_list'),
    path('novo_jogo', views.JogosCreateView.as_view(), name='new_game'),
    path('update_jogo/<int:pk>/', views.JogosUpdateView.as_view(), name='update_game'),
    path('delete_jogo/<int:pk>/', views.jogosDelete, name='delete_game'),
    path('nova_equipa', views.EquipaCreateView.as_view(), name='new_team'),
    path('update_equipa/<int:pk>/', views.EquipaUpdateView.as_view(), name='update_team'),
    path('delete_equipa/<int:pk>/', views.equipaDelete, name='delete_team'),
    path('estatistica_jogo/<int:pk>/', views.estatistica_jogo, name='estatistica_jogo'),
    path('iniciar_jogo/<int:id_jogo>', views.iniciar_jogo, name='iniciar_jogo'),
    path('substituicao_jogo/', views.substituicao_jogo, name='substituicao_jogo'),
    path('intervalo_jogo/<int:id_jogo>/', views.intervalo_jogo, name='intervalo_jogo'),
    path('finalizar_jogo/<int:id_jogo>/', views.finalizar_jogo, name='finalizar_jogo'),
    path('golo/<int:atleta_id>/<int:jogo_id>/', views.golo, name='golo'),
    path('golo_equipa/<int:id_jogo>/<int:id_equipa>/', views.golo_equipa, name='golo_equipa'),
]



