# Pokemon Crawler

Project started from https://docs.docker.com/compose/django/

Some useful commands:

* `docker-compose up`
* `docker-compose exec web bash`
* `docker-compose exec web python -m pip install -r requirements.txt`

# How to crawl Pokemons and view the Pokemons stored in the DB
- Run `docker-compose up` to start the app.
- Open a new terminal window and run `docker-compose exec web bash` to get into the container app.
- Run the command `python manage.py crawl_pokemon --page=<page_number>` where `page_number` is the page you want to grab from the PokeAPI.
- You must see the crawled pokemons visiting the URL http://localhost:8000/. Use the pagination provided in the website if neccesary. Just click on the Pokemon name to check the pokemon details.
