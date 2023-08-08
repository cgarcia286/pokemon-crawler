from django.contrib import admin

from .models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ['name', 'id_reference']
    list_per_page = 20
