"""
reputation.tests.tests
"""
from django.utils.unittest.case import TestCase
from django.contrib.auth.models import User

from reputation.models import Reputation

from .models import Content
from .reputation_indexes import ContentReputationHandler

class TestModels(TestCase):
    def setUp(self):
        self.user = User(username="gigi")
        self.user.save()

        content = Content(user=self.user)
        content.save()

    def test_basic_reputation(self):
        score = Reputation.objects.reputation_for_user(
            ContentReputationHandler.dimension,
            self.user
        ).reputation
        self.assertEqual(score, ContentReputationHandler.VALUE)
