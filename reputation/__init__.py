import inspect

from django.utils import importlib
from django.conf import settings

from reputation.sites import site  # do not remove

VERSION = (0, 1, None)
__version__ = VERSION


def autodiscover():
    """
    Automatically build the reputation index.

    Almost exactly as django.contrib.admin does things, for consistency.
    """
    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        # For each app, we need to look for an reputation_indexes.py inside
        # that app's package. We can't use os.path here -- recall that modules
        # may be imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for reputation_indexes.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own index registration.
        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's reputation_indexes.py.
        # For some reason imp.find_module raises ImportError if the app can't
        # be found but doesn't actually try to import the module. So skip this
        # app if its reputation_indexes.py doesn't exist
        try:
            imp.find_module('reputation_indexes', app_path)
        except ImportError:
            continue

        # Step 3: import the app's reputation_index file. If this has errors
        # we want them to bubble up.
        importlib.import_module("%s.reputation_indexes" % app)


def handle_reputation_registrations(*args, **kwargs):
    """
    Ensures that any configuration of the ReputationSites(s) are handled when
    importing django-reputation.

    This makes it possible for scripts/management commands that affect models
    but know nothing of Haystack to keep the index up to date.
    """
    if not getattr(settings, 'REPUTATION_ENABLE_REGISTRATIONS', True):
        # If the user really wants to disable this, they can, possibly at their
        # own expense. This is generally only required in cases where other
        # apps generate import errors and requires extra work on the user's
        # part to make things work.
        return

    # This is a little dirty but we need to run the code that follows only
    # once, no matter how many times the main Reputation module is imported.
    # We'll look through the stack to see if we appear anywhere and simply
    # return if we do, allowing the original call to finish.
    stack = inspect.stack()

    for stack_info in stack[1:]:
        if 'handle_reputation_registrations' in stack_info[3]:
            return

    # Pull in the config file, causing any SearchSite initialization code to
    # execute.
    search_sites_conf = importlib.import_module(settings.REPUTATION_SITECONF)


handle_reputation_registrations()
