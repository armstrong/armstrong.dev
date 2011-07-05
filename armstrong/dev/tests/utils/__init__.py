from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from armstrong.dev.tests.utils.base import ArmstrongTestCase, override_settings