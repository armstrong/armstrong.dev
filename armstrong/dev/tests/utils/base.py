from django.test import TestCase as DjangoTestCase
from django.db import models

# DEPRECATED remove when we drop Django 1.3 support
# Backport override_settings from Django 1.4
try:
    from django.test.utils import override_settings
except ImportError:
    from .backports import override_settings

# If the component uses fudge, provide useful shared behavior
try:
    import fudge
    hasFudge = True
except ImportError:
    hasFudge = False


class ArmstrongTestCase(DjangoTestCase):
    if hasFudge:
        def setUp(self):
            fudge.clear_expectations()
            fudge.clear_calls()

    # DEPRECATED remove when we drop Django 1.3 support
    if not hasattr(DjangoTestCase, 'settings'):
        # backported from Django 1.4
        def settings(self, **kwargs):
            """
            A context manager that temporarily sets a setting and reverts
            back to the original value when exiting the context.

            .. seealso: https://github.com/django/django/blob/0d670682952fae585ce5c5ec5dc335bd61d66bb2/django/test/testcases.py#L349-354
            """
            return override_settings(**kwargs)

    def assertRelatedTo(self, model, field_name, related_model, many=False):
        if many is False:
            through = models.ForeignKey
        else:
            through = models.ManyToManyField

        # sanity check
        self.assertModelHasField(model, field_name, through)

        field = model._meta.get_field_by_name(field_name)[0]
        self.assertEqual(field.rel.to, related_model)

    def assertModelHasField(self, model, field_name, field_class=None):
        msg = "%s does not have a field named %s" % (model.__class__.__name__,
                field_name)
        self.assertTrue(hasattr(model, field_name), msg=msg)
        field = model._meta.get_field_by_name(field_name)[0]
        if field_class is not None:
            msg = "%s.%s is not a %s" % (model.__class__.__name__, field_name,
                    field_class.__class__.__name__)
            self.assertTrue(isinstance(field, field_class), msg=msg)
