"""Helper functions for the pokemons app"""
from typing import Union
import requests

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .models import Pokemon

POKEAPI_V2_BASE_URL = getattr(settings, 'POKEAPI_V2_BASE_URL', None)


@transaction.atomic
def crawl_pokemons(page: int) -> None:
    """
    Helper function to crawl pokemons data from the PokeAPI and store them in the DB
    """
    if POKEAPI_V2_BASE_URL is None:
        raise ImproperlyConfigured('POKEAPI_V2_BASE_URL must be defined on the project settings')

    size = 20
    offset = page * size

    response = requests.get(f'{POKEAPI_V2_BASE_URL}pokemon/?offset={offset}&limit={size}')
    if response.status_code == 200:
        data = response.json()

        pokemons = []
        for pokemon_data in data['results']:
            pokemon_details = requests.get(pokemon_data['url']).json()
            description = _get_pokemon_description(pokemon_details['id'])
            abilities = _get_names_from_data(pokemon_details['abilities'], 'ability')
            stats = _get_names_from_data(pokemon_details['stats'], 'stat', True)
            movements = _get_names_from_data(pokemon_details['moves'], 'move')
            image = pokemon_details['sprites']['front_default']

            # Update Pokemon if already exists, otherwise add create a new Pokemon object and
            # add it to a list to perform a bulk create
            try:
                pokemon = Pokemon.objects.get(id_reference=pokemon_details['id'])

            except Pokemon.DoesNotExist:
                pokemons.append(
                    Pokemon(
                        name=pokemon_details['name'],
                        id_reference=pokemon_details['id'],
                        description=description,
                        abilities=abilities,
                        stats=stats,
                        movements=movements,
                        image=image
                    )
                )

            else:
                pokemon.name = pokemon_details['name']
                pokemon.description = description
                pokemon.abilities = abilities
                pokemon.stats = stats
                pokemon.movements = movements
                pokemon.image = image
                pokemon.save()

        Pokemon.objects.bulk_create(pokemons)


def _get_pokemon_species_data(pokemon_id: int) -> Union[dict, None]:
    """
    Fetches information about a specific Pokemon species from the PokeAPI.

    Args:
        pokemon_id (int): The unique identifier of the Pokemon species.

    Returns:
        Union[dict, None]: A dictionary containing information about the Pokemon species,
        or None if the API request was unsuccessful.
    """
    response = requests.get(f'{POKEAPI_V2_BASE_URL}pokemon-species/{pokemon_id}/')
    if response.status_code == 200:
        return response.json()
    else:
        return None


def _get_english_description(pokemon_species_data: dict) -> Union[str, None]:
    """
    Retrieve the English description for a given Pokemon species data.

    Args:
        pokemon_species_data (dict): A dictionary containing information about a Pokemon species.

    Returns:
        str: The English flavor text description of the Pokemon species. If no English flavor
        text is found, returns None.
    """
    for flavor_text_entry in pokemon_species_data['flavor_text_entries']:
        if flavor_text_entry['language']['name'] == 'en':
            return flavor_text_entry['flavor_text']
    return None


def _get_pokemon_description(pokemon_id):
    """
    Retrieve the English flavor text description for a Pokémon based on its ID or name.

    This function obtains species data for the specified Pokémon using its ID or name,
    then retrieves the English flavor text description if available.

    Args:
        pokemon_id (int): The ID of the Pokémon.

    Returns:
        str: The English flavor text description of the Pokémon. If the Pokémon data is not found
        or no English flavor text is available, returns None.
    """
    species_data = _get_pokemon_species_data(pokemon_id)
    if species_data:
        description = _get_english_description(species_data)
        return description
    return None


def _get_names_from_data(data: list, key: str, base_stat: bool = False) -> str:
    """
    Retrieve names from a list of data elements based on the specified key.

    Args:
        data (list): List of data elements.
        key (str): Key to access the name in each data element.
        base_stat (bool, optional): Indicates whether to include base stats. Defaults to False.

    Returns:
        str: Comma-separated string containing the retrieved names.
    """
    if base_stat:
        names = [f'{element[key]["name"]}: {element["base_stat"]}' for element in data]
    else:
        names = [element[key]["name"] for element in data]

    return ', '.join(names)
