from django.views.generic import DetailView, ListView

from .models import Pokemon

POKE_API_BASE_URL = 'https://pokeapi.co/api/v2'


class PokemonsListView(ListView):
    model = Pokemon
    template_name = 'index.html'
    context_object_name = 'pokemons'
    paginate_by = 20


class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = 'pokemon-detail.html'
    context_object_name = 'pokemon'
