from reputation.exceptions import AlreadyRegistered, NotRegistered


class ReputationSite(object):
    """
    Encapsulates all the indexes that should be available.

    This allows you to register indexes on models you don't control (reusable
    apps, django.contrib, etc.) as well as customize on a per-site basis what
    indexes should be available (different indexes for different sites, same
    codebase).

    A SearchSite instance should be instantiated in your URLconf, since all
    models will have been loaded by that point.

    The API intentionally follows that of django.contrib.admin's AdminSite as
    much as it makes sense to do.
    """

    def __init__(self):
        self._registry = {}
        self._cached_field_mapping = None

    def register(self, model, index_class=None):
        """
        Registers a model with the site.

        The model should be a Model class, not instances.

        If no custom index is provided, a generic SearchIndex will be applied
        to the model.
        """
        if not index_class:
            ## TODO: mmmmh
            from haystack.indexes import BasicSearchIndex
            index_class = BasicSearchIndex

        if not hasattr(model, '_meta'):
            raise AttributeError('The model being registered must derive from Model.')

        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__class__)

        self._registry[model] = index_class(model)
#        self._setup(model, self._registry[model])

    def unregister(self, model):
        """
        Unregisters a model from the site.
        """
        if model not in self._registry:
            raise NotRegistered('The model %s is not registered' % model.__class__)
#        self._teardown(model, self._registry[model])
        del(self._registry[model])


site = ReputationSite()
