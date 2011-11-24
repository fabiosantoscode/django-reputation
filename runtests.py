#!/usr/bin/env python

"""
runtests
~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import sys
from django.core.management import call_command
from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            },
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.sites',

            # Included to fix Disqus' test Django which solves IntegrityMessage case
            'django.contrib.contenttypes',
            'reputation',

            'tests',
            'django_jenkins',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        TEMPLATE_DEBUG=True,
        REPUTATION_SITECONF="tests.siteconf",
        JENKINS_TASKS=(
#            'django_jenkins.tasks.run_pylint',
#            'django_jenkins.tasks.run_pep8',
#            'django_jenkins.tasks.with_coverage',
            'django_jenkins.tasks.django_tests',
        ),
    )

def runtests(*test_args):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

#    if not test_args:
#        test_args = ['tests']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    val = call_command('jenkins', 'tests', verbosity=1, interactive=True)
#    failures = run_tests(test_args)
#    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
