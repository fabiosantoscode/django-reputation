"""
reputation.tests.tests
"""
from django.utils.unittest.case import TestCase
from django.contrib.auth.models import User

from reputation.models import Reputation, ReputationAction
from reputation.conf import settings

from .models import Content, DownContent
from .reputation_indexes import ContentReputationHandler

class TestModels(TestCase):
    def setUp(self):
        self.user = User(username="gigi")
        self.user.save()
        self.dimension = ContentReputationHandler.dimension

    def tearDown(self):
        self.user.delete()

    def _get_score(self, user=None, dim=None):
        if user is None:
            user = self.user
        if dim is None:
            dim = self.dimension
        return Reputation.objects.reputation_for_user(
            dim, user
        ).reputation

    def test_basic_reputation(self):
        score = self._get_score()
        self.assertEqual(score, 0)

        content = Content(user=self.user)
        content.save()

        score = self._get_score()
        self.assertEqual(score, ContentReputationHandler.VALUE)

    def test_reputation_remove_target_object(self):
        """
        test that if the object that gives reputation is removed, the
        reputation is removed
        """
        self.assertEqual(self._get_score(), 0)

        content = Content(user=self.user)
        content.save()

        self.assertGreater(self._get_score(), 0)

        content.delete()
        self.assertEqual(self._get_score(), 0)

    def test_max_gain_per_day(self):
        """
        test max gain per day
        """
        score = self._get_score()
        self.assertEqual(score, 0)

        for i in range(50):
            content = Content(user=self.user)
            content.save()

        score = self._get_score()
        self.assertEqual(score, settings.REPUTATION_MAX_GAIN_PER_DAY)

    def test_max_loss_per_day(self):
        score = self._get_score()
        self.assertEqual(score, 0)

        for i in range(50):
            content = DownContent(user=self.user)
            content.save()

        score = self._get_score()
        self.assertEqual(score, -1*settings.REPUTATION_MAX_LOSS_PER_DAY)

