from unittest.mock import MagicMock, patch

from django.test import TestCase

from ..models import Pokemon
from .. import utils


class TestPokemonUtils(TestCase):
    def setUp(self):
        self.pokemon_data = {
            'results': [
                {
                    'name': 'bulbasaur',
                    'url': 'https://pokeapi.co/api/v2/pokemon/1/'
                },
                {
                    'name': 'ivysaur',
                    'url': 'https://pokeapi.co/api/v2/pokemon/2/'
                }
            ]
        }
        self.pokemon_details = {
            'id': 1,
            'name': 'bulbasaur',
            'abilities': [{'ability': {'name': 'chlorophyll'}}, {'ability': {'name': 'overgrow'}}],
            'stats': [{'base_stat': 45, 'stat': {'name': 'hp'}}, {'base_stat': 65, 'stat': {'name': 'attack'}}],
            'moves': [{'move': {'name': 'tackle'}}, {'move': {'name': 'vine-whip'}}]
        }
        self.pokemon_species_data = {
            'flavor_text_entries': [
                {'language': {'name': 'en'}, 'flavor_text': 'Bulbasaur description'}
            ]
        }

    @patch('pokemons.utils.requests.get')
    def test_crawl_pokemons(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.pokemon_data

        mock_pokemon_details_response = MagicMock()
        mock_pokemon_details_response.status_code = 200
        mock_pokemon_details_response.json.return_value = self.pokemon_details
        mock_get.side_effect = [mock_pokemon_details_response * len(self.pokemon_data['results'])]

        mock_species_data_response = MagicMock()
        mock_species_data_response.status_code = 200
        mock_species_data_response.json.return_value = self.pokemon_species_data
        utils._get_pokemon_species_data = MagicMock(return_value=mock_species_data_response)

        utils.crawl_pokemons(page=0)

        self.assertEqual(Pokemon.objects.count(), len(self.pokemon_data['results']))

    @patch('requests.get')
    def test_get_english_description(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.pokemon_species_data

        description = utils._get_english_description(self.pokemon_species_data)
        self.assertEqual(description, 'Bulbasaur description')

    @patch('pokemons.utils.requests.get')
    def test_get_pokemon_description(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.pokemon_species_data

        description = utils._get_pokemon_description(pokemon_id=1)
        self.assertEqual(description, 'Bulbasaur description')

    def test_get_names_from_data(self):
        data = [
            {'ability': {'name': 'chlorophyll'}},
            {'ability': {'name': 'overgrow'}}
        ]
        names = utils._get_names_from_data(data, key='ability')
        self.assertEqual(names, 'chlorophyll, overgrow')

        base_stat_data = [
            {'base_stat': 45, 'stat': {'name': 'hp'}},
            {'base_stat': 65, 'stat': {'name': 'attack'}}
        ]
        base_stat_names = utils._get_names_from_data(base_stat_data, key='stat', base_stat=True)
        self.assertEqual(base_stat_names, 'hp: 45, attack: 65')
