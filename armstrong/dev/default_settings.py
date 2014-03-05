# Since we are using configure() we need to manually load the defaults
from django.conf.global_settings import *

# Grab our package information
import json
package = json.load(open("./package.json"))
app_name = package['name'].rsplit('.', 1)[1]


#
# Default settings
#
INSTALLED_APPS = [package['name']]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": 'mydatabase'
    }
}
TEST_RUNNER = "armstrong.dev.tests.runner.ArmstrongDiscoverRunner"

COVERAGE_EXCLUDE_FILES = ['*/migrations/*']

#
# A component may override settings by creating an `env_settings.py`
# file in its root directory that imports from this file.
#
#     from armstrong.dev.default_settings import *
#
