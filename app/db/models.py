"""Common models for all pokemon-crawler apps"""
from uuid import uuid4

from django.db import models


class TimeStampModel(models.Model):
    """
    Create fields to keep track when objects were created
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomIdModel(TimeStampModel):
    """
    Replace id integer field by an UUID field and includes TimeStampModel to keep track of
    creation and update timestamps
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True
