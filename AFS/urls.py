
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('apps.atletas.urls')),
    path('eumandoaqui/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('jogos/', include('apps.jogos.urls')),
    path('equipamentos/', include('apps.equipamentos.urls',namespace='equipamentos')),
    path('core/', include('apps.core.urls')),
    path('atletas/', include('apps.atletas.urls',namespace='atletas')),
]
