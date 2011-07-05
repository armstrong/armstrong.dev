from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from django.test import TestCase as DjangoTestCase
import fudge


# Backport override_settings from Django 1.4 
try:
    from django.test.utils import override_settings

except ImportError:
    from django.conf import settings, UserSettingsHolder
    from django.utils.functional import wraps


    class override_settings(object):
        """
        Acts as either a decorator, or a context manager. If it's a decorator it
        takes a function and returns a wrapped function. If it's a contextmanager
        it's used with the ``with`` statement. In either event entering/exiting
        are called before and after, respectively, the function/block is executed.
        """
        def __init__(self, **kwargs):
            self.options = kwargs
            self.wrapped = settings._wrapped

        def __enter__(self):
            self.enable()

        def __exit__(self, exc_type, exc_value, traceback):
            self.disable()

        def __call__(self, test_func):
            from django.test import TestCase
            if isinstance(test_func, type) and issubclass(test_func, TestCase):
                class inner(test_func):
                    def _pre_setup(innerself):
                        self.enable()
                        super(inner, innerself)._pre_setup()
                    def _post_teardown(innerself):
                        super(inner, innerself)._post_teardown()
                        self.disable()
            else:
                @wraps(test_func)
                def inner(*args, **kwargs):
                    with self:
                        return test_func(*args, **kwargs)
            return inner

        def enable(self):
            override = UserSettingsHolder(settings._wrapped)
            for key, new_value in self.options.items():
                setattr(override, key, new_value)
            settings._wrapped = override

        def disable(self):
            settings._wrapped = self.wrapped
    



class ArmstrongTestCase(DjangoTestCase):
    def setUp(self):
        fudge.clear_expectations()
        fudge.clear_calls()

    # backported from Django 1.4, should probably have some kind of __hasattr__ test
    def settings(self, **kwargs):
        return override_settings(**kwargs)
