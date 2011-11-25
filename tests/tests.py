"""
reputation.tests.tests
"""
from django.utils.unittest.case import TestCase
from django.contrib.auth.models import User

from reputation.models import Reputation, ReputationAction

from .models import Content
from .reputation_indexes import ContentReputationHandler

class TestModels(TestCase):
    def setUp(self):
        self.user = User(username="gigi")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_basic_reputation(self):
        score = Reputation.objects.reputation_for_user(
            ContentReputationHandler.dimension,
            self.user
        ).reputation
        self.assertEqual(score, 0)

        content = Content(user=self.user)
        content.save()

        score = Reputation.objects.reputation_for_user(
            ContentReputationHandler.dimension,
            self.user
        ).reputation
        self.assertEqual(score, ContentReputationHandler.VALUE)
