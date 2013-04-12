# Since we are using configure() we need to manually load the defaults
from django.conf.global_settings import *

# Grab our package information
import json
package = json.load(open("./package.json"))


#
# Default settings
#
DEBUG = True
TESTED_APPS = ['tests']
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
    }
}


#
# Component specific settings
#
# Each component needs to create an `env_settings.py` file in its
# root directory that imports this file. Then the component can define
# whatever it needs for its Django environment. example:
#
# from armstrong.dev.default_settings import *
#
# INSTALLED_APPS = [
#     package["name"],
#     '%s.tests' % package["name"],
# ]
#
