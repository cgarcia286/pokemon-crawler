from django.core.management.base import BaseCommand, CommandError
from pokemons.utils import crawl_pokemons


class Command(BaseCommand):
    """
    Custom Django command to crawl and store Pokemon data from the PokeAPI.

    Usage:
        python manage.py crawl_pokemon --page=<page_number>

    Arguments:
        --page=<page_number>: The pagination page number to retrieve data from PokeAPI.

    Example:
        python manage.py crawl_pokemon --page=2

    """
    help = 'Crawl and store Pokemon data from the PokeAPI'

    def add_arguments(self, parser):
        """
        Adds optional arguments to the command.

        Args:
            parser: ArgumentParser instance.
        """
        parser.add_argument('--page', type=int, help='Pagination to get data from PokeAPI')

    def handle(self, *args, **options):
        """
        Handles the execution of the command.

        Args:
            *args: Additional arguments.
            **options: Command options.

        Raises:
            CommandError: If page number is not specified in the command options.
        """
        if options['page'] is None:
            raise CommandError('You must specify a page number to crawl Pokemon data')

        crawl_pokemons(options['page'])
        self.stdout.write(self.style.SUCCESS('Successfully crawled Pokemon data'))
