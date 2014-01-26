#!/usr/bin/env python
import os
import sys

try:
    from django.conf import settings
except ImportError as e:
    raise ImportError("%s. Check to see if Django "
        "is installed in your virtualenv." % e)


__all__ = ['run_django_cmd']


# Add the component's directory to the path so we can import from it
sys.path.append(os.getcwd())

try:
    import env_settings as package_settings
except ImportError as e:
    print("Could not find component specific settings file. "
        "Using armstrong.dev defaults...")
    try:
        import armstrong.dev.default_settings as package_settings
    except ImportError as e:
        raise ImportError("%s. Running a Django environment for this "
            "component requires either an `env_settings.py` file or the "
            "armstrong.dev `default_settings.py` file." % e)


# Setup the Django environment
if not settings.configured:
    settings.configure(default_settings=package_settings)


def determine_test_args(test_labels):
    """
    Limit testing to settings.TESTED_APPS if available while behaving
    exactly like `manage.py test` and retaining Django's ability to
    explicitly provide test apps/cases/methods on the commandline.

    """
    return test_labels or getattr(settings, 'TESTED_APPS', [])


# Import access
def run_django_cmd(cmd, *args, **kwargs):
    if cmd == "test":
        args = determine_test_args(args)

    from django.core.management import call_command
    return call_command(cmd, *args, **kwargs)


# Commandline access
def run_django_cli():
    args = sys.argv[2:]

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # anything not a flag (e.g. -v, --version) is treated as a named test
        # (it'll be a short list so iterating it twice is okay)
        args = [arg for arg in sys.argv[2:] if arg.startswith('-')]
        test_labels = [arg for arg in sys.argv[2:] if not arg.startswith('-')]
        args = determine_test_args(test_labels) + args

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv[:2] + args)


if __name__ == "__main__":
    run_django_cli()
