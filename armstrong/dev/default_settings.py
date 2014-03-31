"""
Default settings for Armstrong components running in a dev/test environment

A component may (and might have to) override or supply additional settings
by creating an `env_settings.py` file in its root directory that imports
from this file.

    from armstrong.dev.default_settings import *

"""
# Since we are using configure() we need to manually load the defaults
from django.conf.global_settings import *

# Grab our package information
import json
package = json.load(open("./package.json"))
app_name = package['name'].rsplit('.', 1)[1]

#
# Armstrong default settings
#
DEBUG = True
INSTALLED_APPS = [package['name']]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": 'mydatabase'
    }
}
TEST_RUNNER = "armstrong.dev.tests.runner.ArmstrongDiscoverRunner"

COVERAGE_EXCLUDE_FILES = ['*/migrations/*']

# Add a DEBUG console "armstrong" logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {'format': '%(levelname)s %(name)s--%(message)s'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'basic'
        }
    },
    'loggers': {
        'armstrong': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}
