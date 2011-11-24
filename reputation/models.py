import datetime
from operator import itemgetter

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel

from reputation.conf import settings


REPUTATION_MAX_GAIN_PER_DAY = settings.REPUTATION_MAX_GAIN_PER_DAY
REPUTATION_MAX_LOSS_PER_DAY = settings.REPUTATION_MAX_LOSS_PER_DAY


def dimension_to_short_dimension(dimension):
    """
    Given a long description (eg. "contributor"), returns the short dimension

    >>> dimension_to_short_dimension("contributor")
    "CO"
    """
    l_dimension = settings.REPUTATION_DIMENSIONS.items()
    return l_dimension[map(itemgetter(1), l_dimension).index(dimension)][0]


class ReputationManager(models.Manager):
    """
    Custom manager for the "Reputation" model.

    Methods defined here provide shortcuts for modifying and tracking the
    reputation of users.
    """

    def reputation_for_user(self, dimension, user):
        """
        Returns the "Reputation" object associated with a "User".

        if no "Reputation" object currently exists for the user,
        then attempt to create a new "Reputation" object with default
        values.
        """
        dim_short = dimension_to_short_dimension(dimension)
        try:
            reputation_object = user.reputation_set.get(dimension=dim_short)
        except ObjectDoesNotExist:
            reputation_object = Reputation(user=user, dimension=dim_short)
            reputation_object.save()
        return reputation_object

    def calculate_reputation_for_today(self, dimension, user):
        """
        Calculates and returns the total amount of reputation a User
        has gained today.
        """
        today = datetime.datetime.today
        start_time = today().replace(hour=0, minute=0, second=0)
        end_time = today().replace(hour=23, minute=59, second=59)

        relevant_reputation_actions = ReputationAction.objects.filter(
            dimension=dimension_to_short_dimension(dimension),
            user=user,
            created__range=(start_time, end_time)
        )
        # TODO: use Sum() aggregate

        delta = sum([action.value for action in relevant_reputation_actions])
        return delta

    def update_reputation(self, dimension, user, value):
        """
        Updates an "User"s associated "Reputation" object by adding value to
        the user's current reputation.

        if value == 0, then nothing is done.
        """
        if value:
            reputation = self.reputation_for_user(dimension, user)
            reputation.reputation = value
            reputation.save()

    def log_reputation_action(self, dimension, user, originating_user,
                              action_value, target_object, created):
        """
        Attempt to create a ReputationAction object associated with @user

        if a ReputationAction is found and uniqueness constraints checking
        passes, then attempt to update @user's reputation.  Checks the current
        reputation gained today and limits the change in reputation if the
        user has outbounded either REPUTATION_MAX_GAIN_PER_DAY or
        REPUTATION_MAX_LOSS_PER_DAY.
        """
        content_type_object = ContentType.objects.get_for_model(
            target_object.__class__
        )
        object_id = target_object.id

        kwargs = dict(created=created)
        reputation_action = ReputationAction(
            dimension=dimension_to_short_dimension(dimension),
            user=user,
            originating_user=originating_user,
            content_type=content_type_object,
            object_id=object_id,
            value=action_value,
            **kwargs
        )
        reputation_action.save()

        today_delta = Reputation.objects.calculate_reputation_for_today(
            dimension, user
        )
        expected_delta = action_value + today_delta

        value = max(
            -1*REPUTATION_MAX_LOSS_PER_DAY,
                min(expected_delta, REPUTATION_MAX_GAIN_PER_DAY)
        )
        Reputation.objects.update_reputation(dimension, user, value)

#    def update_user_reputation(self, user, final_value):
#        """
#        Updates target @user's reputation to @final_value.
#        """
#        reputation_object = self.reputation_for_user(user)
#        reputation_object.reputation = final_value
#        reputation_object.save()


class Reputation(TimeStampedModel):
    """
    Model for storing a "User" object's reputation in an IntegerField.
    """
    reputation = models.IntegerField(default = 0)
    user = models.ForeignKey(User, related_name='reputation_set')
    dimension = models.CharField(max_length=2, blank=True, null=True)

    objects = ReputationManager()

    def save(self, **kwargs):
        super(Reputation, self).save(**kwargs)
        permissions = []
        for permission, reputation in settings.REPUTATION_PERMISSIONS.items():
            if self.reputation > reputation:
                permissions.append(permission)
        self.user.permissions = permissions

    def __unicode__(self):
        return u"%s - %s" % (self.user.username, unicode(self.reputation))


class ReputationAction(TimeStampedModel):
    """
    Model representing an action a user takes that effects the user's
    reputation.
    """
    user = models.ForeignKey(User, related_name='target_user')
    originating_user = models.ForeignKey(User,
                                         related_name='originating_user',
                                         null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    dimension = models.CharField(max_length=2, blank=True, null=True)
    value = models.IntegerField(default = 0)

    def __unicode__(self):
        return u"%s - %d" % (self.user.username, self.value)
