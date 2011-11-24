"""
Rebuild reputation
"""
from django.core.management.base import BaseCommand

from reputation import site
from reputation.models import Reputation, ReputationAction


class Command(BaseCommand):
    """
    Rebuild reputation index
    """

    def handle(self, *args, **kwargs):
        """
        BaseCommand.handle() contains the logic of management commands
        """
        Reputation.objects.all().delete()
        ReputationAction.objects.all().delete()

        for Model, handler in site._registry.iteritems():
            for obj in handler.index_queryset():
                handler.modify_reputation(obj)

