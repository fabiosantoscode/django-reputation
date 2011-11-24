"""
List User reputations
"""
from django.contrib.auth.models import User

from django.core.management.base import BaseCommand

from reputation.conf import settings
from reputation.models import Reputation


class Command(BaseCommand):
    """
    List reputations
    """

    def handle(self, *args, **kwargs):
        """
        BaseCommand.handle() contains the logic of management commands
        """
        for short_dim, dim in settings.REPUTATION_DIMENSIONS.items():
            print "=== %s ===" % (dim,)
            for user in User.objects.filter(is_active=True):
                print user, Reputation.objects.reputation_for_user(
                    dim, user).reputation
            print ''
