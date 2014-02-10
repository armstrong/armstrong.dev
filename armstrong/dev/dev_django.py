#!/usr/bin/env python
import os
import sys
import threading
from functools import wraps


__all__ = ['run_django_cmd', 'run_django_cli', 'DjangoSettings']


class DjangoSettings(object):
    """
    Isolate settings import so it doesn't happen on module import.

    Not all of our tasks need Django so we only want to build up
    our component environment's settings if and when they are needed.
    This approach avoids unnecessary warnings if the settings aren't
    available or Django isn't installed.

    Do this as a singleton to avoid trying our imports and running
    configure() over and over, but note that the object returned is
    still the typical ``django.conf.LazySettings`` and so settings
    remain mutable.

    """
    _singleton_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Threadsafe singleton loading of settings"""

        if not cls._instance:
            with cls._singleton_lock:
                if not cls._instance:
                    cls._instance = cls.load_settings()
        return cls._instance

    @staticmethod
    def load_settings():
        try:
            from django.conf import settings
        except ImportError as e:
            raise ImportError(
                "%s. Check to see if Django is installed in your "
                "virtualenv." % e)

        # Add the component's directory to the path so we can import from it
        sys.path.append(os.getcwd())

        try:
            import env_settings as package_settings
        except ImportError as e:
            print(
                "Could not find component specific settings file. "
                "Using armstrong.dev defaults...")
            try:
                from . import default_settings as package_settings
            except ImportError as e:
                raise ImportError(
                    "%s. Running a Django environment for this component "
                    "requires either an `env_settings.py` file or "
                    "`armstrong.dev.default_settings.py`." % e)

        # Setup the Django environment
        if not settings.configured:
            settings.configure(default_settings=package_settings)

        return settings


def load_django_settings(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        DjangoSettings()
        return func(*args, **kwargs)
    return wrapper


# Import access
@load_django_settings
def run_django_cmd(cmd, *args, **kwargs):
    from django.core.management import call_command
    return call_command(cmd, *args, **kwargs)


# Commandline access
@load_django_settings
def run_django_cli(argv=None):
    argv = argv or sys.argv

    from django.core.management import execute_from_command_line
    execute_from_command_line(argv)


if __name__ == "__main__":
    run_django_cli()
