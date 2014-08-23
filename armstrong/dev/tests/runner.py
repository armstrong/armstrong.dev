try:
    from django.test.runner import DiscoverRunner
except ImportError:  # DROP_WITH_DJANGO15
    from .utils.runner import DiscoverRunner


class ArmstrongDiscoverRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        """Find our "tests" package, not just "test*.py" files"""

        super(ArmstrongDiscoverRunner, self).__init__(*args, **kwargs)
        self.pattern = "test*"
