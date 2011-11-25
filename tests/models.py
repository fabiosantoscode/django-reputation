"""
reputation.tests
"""
from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel


class Content(TimeStampedModel):
    """
    test models
    """
    user = models.ForeignKey(User)
