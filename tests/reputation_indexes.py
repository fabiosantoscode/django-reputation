"""
Reputation index for reputation.tests
"""

from reputation.handlers import BaseReputationHandler
from reputation import site

from .models import Content

class ContentReputationHandler(BaseReputationHandler):
    """
    Reputation Handler for user contents
    """
    model = Content
    VALUE = 10
    dimension = 'contributor'

    def check_conditions(self, instance):
        return True

    def get_target_object(self, instance):
        return instance

    def get_target_user(self, instance):
        return instance.user

    def get_originating_user(self, instance):
        return None

    def get_value(self, instance):
        return self.VALUE

site.register(Content, ContentReputationHandler)
