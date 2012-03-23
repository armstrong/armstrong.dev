import django
import os, sys

DEFAULT_SETTINGS = {
    'DATABASE_ENGINE': 'sqlite3',
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase'
        }
    },
}

class VirtualDjango(object):
    def __init__(self,
                 caller=sys.modules['__main__'],
                 default_settings=DEFAULT_SETTINGS):
        self.caller = caller
        self.default_settings = default_settings


    def configure_settings(self, customizations, reset=True):
        # Django expects a `DATABASE_ENGINE` value
        custom_settings = self.default_settings
        custom_settings.update(customizations)

        settings = self.settings
        if reset:
            self.reset_settings(settings)
        settings.configure(**custom_settings)

    def reset_settings(self, settings):
        if django.VERSION[:2] == (1, 3):
            settings._wrapped = None
            return

        # This is the way to reset settings going forward
        from django.utils.functional import empty
        settings._wrapped = empty
        
    @property
    def settings(self):
        from django.conf import settings
        return settings

    @property
    def call_command(self):
        from django.core.management import call_command
        return call_command

    def run(self, my_settings):
        if hasattr(self.caller, 'setUp'):
            self.caller.setUp()

        self.configure_settings(my_settings)
        return self.call_command
 
