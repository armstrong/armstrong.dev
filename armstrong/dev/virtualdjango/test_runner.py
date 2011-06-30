from armstrong.dev.virtualdjango.base import VirtualDjango

class VirtualDjangoTestRunner(VirtualDjango):
    def run(self, my_settings, *apps_to_test):
        super(VirtualDjangoTestRunner, self).run(my_settings)
        self.call_command('test', *apps_to_test)

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)

run_tests = VirtualDjangoTestRunner()

