from django.urls import path
from . import views

app_name = 'equipamentos'
urlpatterns = [
    path('encomendas_equipamentos/', views.EncomendaEquipamentosListView.as_view(), name='encomendas_equipamentos_list'),
    path('create_encomenda_equipamentos/', views.EncomendaItemCreateView.as_view(), name='create_encomenda_equipamentos'),
    path('create_tamanho/', views.TamanhoCreateView.as_view(), name='create_tamanho'),
    path('update_tamanho/<int:pk>/', views.TamanhoUpdateView.as_view(), name='update_tamanho'),
    path('delete_tamanho/<int:pk>/', views.tamanho_delete, name='delete_tamanho'),
    path('create_equipamentos/', views.EquipamentosCreateView.as_view(), name='create_equipamentos'),
    path('update_equipamentos/<int:pk>/', views.EquipamentosUpdateView.as_view(), name='update_equipamentos'),
    path('delete_equipamentos/<int:pk>/', views.equipamentos_delete, name='delete_equipamentos'),
    path('encomenda_delete/<int:pk>/', views.encomenda_delete, name='encomenda_delete'),
    path('encomendas_por_atleta/<int:pk>/<str:status>/', views.encomendas_por_atleta, name='encomendas_por_atleta'),
    path('encomendas_uptade/<int:pk>/', views.EncomendaUpdateView.as_view(), name='encomendas_uptade'),
    path('alterar_estado_encomenda/<int:pk>/', views.alterar_estado_encomenda, name='alterar_estado_encomenda'),
]

