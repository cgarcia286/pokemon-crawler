"""URL Configuration for pokemons app"""
from django.urls import path

from .views import PokemonDetailView, PokemonsListView

app_name = 'pokemons'

urlpatterns = [
    path('', PokemonsListView.as_view(), name='list'),
    path('detail/<uuid:pk>', PokemonDetailView.as_view(), name='detail'),
]
