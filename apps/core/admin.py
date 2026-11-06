from django.contrib import admin

from .models import Ente


@admin.register(Ente)
class EnteAdmin(admin.ModelAdmin):
    list_display = ["sigla", "nome", "cnpj", "adaptador_dados", "ativo"]
    search_fields = ["sigla", "nome", "cnpj"]
