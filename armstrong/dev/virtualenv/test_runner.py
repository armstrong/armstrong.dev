import pkg_resources
pkg_resources.declare_namespace(__name__)

from armstrong.dev.virtualenv.base import VirtualEnvironment

class VirtualEnvironmentTestRunner(VirtualEnvironment):
    def run(self, my_settings, *apps_to_test):
        super(VirtualEnvironmentTestRunner, self).run(my_settings)
        self.call_command('test', *apps_to_test)

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)

run_tests = VirtualEnvironmentTestRunner()

