import pkg_resources
pkg_resources.declare_namespace(__name__)

import os, sys

ERROR_MESSAGE = """
Error!  You haven't initialized your virtual environment first.

Please run the following to initialize the environment:

    virtualenv .
    pip install -E . -r ./requirements.txt
""".lstrip()

DEFAULT_SETTINGS = {
    'DATABASE_ENGINE': 'sqlite3',
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase'
        }
    },
}

class VirtualEnvironment(object):
    def __init__(self,
                 caller=sys.modules['__main__'],
                 default_settings=DEFAULT_SETTINGS,
                 error_message=ERROR_MESSAGE):
        self.caller = caller
        self.default_settings = default_settings
        self.error_message = error_message
        self._activation_file = None

    @property
    def activation_file(self):
        if not self._activation_file:
            caller_path = os.path.dirname(os.path.realpath(self.caller.__file__))
            if 'bin' == os.path.basename(caller_path):
                caller_path = os.path.dirname(caller_path)
            self._activation_file = os.path.join(caller_path, 'bin', 'activate_this.py')
        return self._activation_file

    @activation_file.setter
    def activation_file(self, v):
        self._activation_file = v

    def activate(self):
        if not os.path.exists(self.activation_file):
            print self.error_message
            sys.exit(1)

        execfile(self.activation_file, dict(__file__=self.activation_file))

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
        self.activate()
        if hasattr(self.caller, 'setUp'):
            self.caller.setUp()

        self.configure_settings(my_settings)
        return self.call_command
 
