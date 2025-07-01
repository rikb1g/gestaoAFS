from django.urls import path
from . import views
from apps.atletas.views import atletas_delete

app_name = 'atletas'

urlpatterns = [
    path('atletas/', views.AtletaListView.as_view(), name='atletas_list'),
    path('create_atleta/', views.AtletaCreateView.as_view(), name='create_atleta'),
    path('atleta_detail/<int:pk>/', views.AtletaDetailView.as_view(), name='atleta_detail'),
    path('update_atleta/<int:pk>/', views.AtletaUpdateView.as_view(), name='update_atleta'),
    path('delete_atleta/<int:pk>/', atletas_delete, name='delete_atleta'),
]