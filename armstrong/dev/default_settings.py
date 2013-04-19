# Since we are using configure() we need to manually load the defaults
from django.conf.global_settings import *

# Grab our package information
import json
package = json.load(open("./package.json"))


#
# Default settings
#
TESTED_APPS = ['tests']
INSTALLED_APPS = [package["name"], 'tests']
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
    }
}

#
# A component may override settings by creating an `env_settings.py`
# file in its root directory that imports from this file.
#
#     from armstrong.dev.default_settings import *
#
