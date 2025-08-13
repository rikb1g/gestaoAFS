from django.contrib import admin
from .models import Equipamentos,Encomenda, EncomendaItem, Tamanho


admin.site.register(Equipamentos)
admin.site.register(Encomenda)
admin.site.register(EncomendaItem)
admin.site.register(Tamanho)