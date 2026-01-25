
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',  include('apps.core.urls'),name="home"),
    path('eumandoaqui/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('jogos/', include('apps.jogos.urls')),
    path('equipamentos/', include('apps.equipamentos.urls',namespace='equipamentos')),
    path('core/', include('apps.core.urls')),
    path('atletas/', include('apps.atletas.urls',namespace='atletas')),
    path('api/', include('apps.api.urls',namespace='api'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)