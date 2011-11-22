"""
Rebuild reputation
"""

from django.core.management.base import BaseCommand

from reputation import site


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
                print obj
