"""app URL Configuration for pokemon-crawler app"""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pokemons.urls', namespace='pokemons'))
]
