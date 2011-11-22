from django.db.models.signals import post_save
from reputation.models import Reputation


class BaseReputationHandler(object):
    """
    Default handler for creating ReputationHandler objects.
    """
    model = None
    dimension = None

    def __init__(self, model=None):
        assert self.dimension, \
            '%s does not define dimension' % (self.__class__,)
        if model:
            self.model = model
        post_save.connect(self._post_save_signal_callback,
            sender=self.model,
            weak=False
        )

    def _post_save_signal_callback(self, **kwargs):
        instance = kwargs['instance']
        created = kwargs['created']
        if created:
            self.modify_reputation(instance)

    def index_queryset(self):
        return self.model.objects.all()

    def check_conditions(self, instance):
        return False

    def get_target_object(self, instance):
        pass

    def get_target_user(self, instance):
        pass

    def get_originating_user(self, instance):
        pass

    def get_value(self, instance):
        return 0

    def modify_reputation(self, instance):
        if self.check_conditions(instance):
            Reputation.objects.log_reputation_action(
                dimension=self.dimension,
                user = self.get_target_user(instance),
                originating_user = self.get_originating_user(instance),
                target_object = self.get_target_object(instance),
                action_value = self.get_value(instance)
            )
