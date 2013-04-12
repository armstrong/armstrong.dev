#!/usr/bin/env python

import sys
from django.conf import settings

try:
    import env_settings as package_settings
except ImportError as e:
    sys.stderr.write("ImportError: %s. Running a Django environment "
        "for this component requires an `env_settings.py` file.\n" % e)


if not settings.configured:
    settings.configure(default_settings=package_settings)


def runtests():
    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(
                verbosity=2,
                interactive=True,
                failfast=False).run_tests(settings.TESTED_APPS)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
