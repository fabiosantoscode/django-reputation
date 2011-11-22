"""
Rebuild reputation
"""
from django.contrib.auth.models import User

from django.core.management.base import BaseCommand

from reputation import site
from reputation.models import Reputation


class Command(BaseCommand):
    """
    Rebuild reputation index
    """

    def handle(self, *args, **kwargs):
        """
        BaseCommand.handle() contains the logic of management commands
        """
        ## TODO: delete old index

        for Model, handler in site._registry.iteritems():
            for obj in handler.index_queryset():
                handler.modify_reputation(obj)

        for user in User.objects.filter(is_active=True):
            print user, Reputation.objects.reputation_for_user(
                'contributor', user).reputation
