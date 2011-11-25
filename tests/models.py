"""
reputation.tests.models
"""

from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel


class Content(TimeStampedModel):
    """
    test model
    """
    user = models.ForeignKey(User)


class DownContent(TimeStampedModel):
    """
    test model
    """
    user = models.ForeignKey(User)
