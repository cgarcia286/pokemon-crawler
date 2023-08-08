"""Model schemas for the pokemons app"""
from django.db import models

from app.db.models import CustomIdModel


class Pokemon(CustomIdModel):
    """
    Schema for the Pokemon Model. This include timestamps for created and updated fields and a
    custom PK based on the CustomIdModel
    """
    id_reference = models.SmallIntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    abilities = models.CharField(max_length=2000)
    stats = models.CharField(max_length=2000)
    movements = models.TextField(max_length=5000)
    image = models.CharField(max_length=2000)

    class Meta:
        ordering = ['id_reference']

    def __str__(self):
        """Returns a string representation for the Pokemon object"""
        return self.name.capitalize()
