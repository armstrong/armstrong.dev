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
            settings._wrapped = None
        settings.configure(**custom_settings)
        
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
 
