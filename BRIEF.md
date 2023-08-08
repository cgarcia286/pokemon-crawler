# Design
In the design of this application, the goal was to create a modular and scalable system that would allow efficient tracking and storage of Pokémon data. To achieve this, an architecture based on the Django framework was chosen, leveraging its capabilities for handling databases, views, and models.

First, the `pokemons` application was created to group the logic responsible for handling the Pokémon search. In this application, the views that manage the graphical interface were defined, which lists the Pokémon found so far, and the details of each of them can be viewed.

Considering that calling this API might take some time (especially when considering that multiple calls might be needed to obtain the required information), a custom command was decided to be used, which can be executed using Django's manage.py utility.

This has the advantage of allowing a CRON job to be run that could collect Pokémon information daily, without the need for user intervention.

The pagination of the results stored in the Database was synchronized with the pagination of the PokeAPI, allowing tracking of discovered Pokémon and enabling the collection of more if required.

The logic for calling the API was separately created in a Python script that groups functions that can be reused to create Pokémon. This enables code reusability in case it's needed in one of the views of the pokemons application since the way of saving information related to Pokémon is always similar.

# Implementation
The implementation was carried out aiming to follow best development practices and standards normally used with Django. As main dependency, the `requests` library was used for making HTTP requests to the PokeAPI. A database model was created to store Pokémon information, based on the challenge requirements.

Values for Pokémon characteristics that represent lists were stored as comma-separated values to allow for coherent reuse when presenting information. The advantage of this format is that it can facilitate value separation using Python's string handling functions if needed in the future.

The custom Django command is responsible for iterating through the PokeAPI results, processing the data, and creating model instances for storage or updating them depending on the scenario.

# Scaling
Regarding scalability, several considerations were taken into account. First, I found that the database used was PostgreSQL, which is great because it facilitates vertical scalability as the amount of data grows. However, to achieve more robust horizontal scalability, the use of a distributed database or a caching solution could be considered to alleviate the load on this database. Furthermore, implementing a queuing system could enable storing all Pokémon data at once, instead of in batches of 20, thus efficiently handling spikes in traffic if a solution is considered where pokemons can be created within the pokemon list view for example in the UI.

Some improvements that can be made in this project include configuring distinct development environments for local and production use, creating separate settings modules and configuration files for each of these environments.

Certainly, establishing a well-defined workflow is essential to ensure the seamless CI/CD of the project. This goal can be accomplished effectively by leveraging tools like GitHub Actions, for instance.

# Testing
For this project, basic unit tests were introduced to safeguard code integrity within the given execution timeframe. While encountering some difficulties in mocking the PokeAPI requests, I opted to retain the failing tests within the project. This approach allows me to shift my focus towards addressing other requirements for this challenge.

Upon careful review of the codebase, unit tests should primarily focus on validating key functions and methods, such as the API carwling function and model instance creation, to ensure the app main funcionality. Creating tests that assert this aspects enhances the development process, giving a greater sense of confidence when implementing new features.

Integration tests need to be created to verify that different components of the application work correctly together, from the tracking utility function to the database.

Finally, pytest-django was chosen as a testing dependency, as it provides more comprehensive tools for execution and error tracing compared to Django's testing system, which can sometimes be a bit simpler.
