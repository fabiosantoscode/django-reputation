"""
Rebuild reputation
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Rebuild reputation index
    """

    def handle(self, *args, **kwargs):
        """
        BaseCommand.handle() contains the logic of management commands
        """
        pass
