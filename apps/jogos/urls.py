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
]