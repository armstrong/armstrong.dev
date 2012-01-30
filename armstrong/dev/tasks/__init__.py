
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)


from contextlib import contextmanager
try:
    import coverage as coverage
except ImportError:
    coverage = False
import os
from os.path import basename, dirname
import sys
from functools import wraps
import unittest

import json

from fabric.api import *
from fabric.colors import red
from fabric.decorators import task

from armstrong.dev.virtualdjango.test_runner import run_tests as run_django_tests
from armstrong.dev.virtualdjango.base import VirtualDjango
from django.core.exceptions import ImproperlyConfigured

if not "fabfile" in sys.modules:
    sys.stderr.write("This expects to have a 'fabfile' module\n")
    sys.stderr.write(-1)
fabfile = sys.modules["fabfile"]


FABRIC_TASK_MODULE = True


__all__ = ["clean", "command", "create_migration", "docs", "pep8", "test",
           "reinstall", "runserver", "shell", "spec", "syncdb", ]

def pip_install(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if getattr(fabfile, "pip_install_first", True):
            with settings(warn_only=True):
                if not os.environ.get("SKIP_INSTALL", False):
                    local("pip uninstall -y %s" % get_full_name(), capture=False)
                    local("pip install .", capture=False)
        func(*args, **kwargs)
    return inner

@contextmanager
def html_coverage_report(directory="./coverage"):
    # This relies on this being run from within a directory named the same as
    # the repository on GitHub.  It's fragile, but for our purposes, it works.
    run_coverage = coverage
    if run_coverage and os.environ.get("SKIP_COVERAGE", False):
        run_coverage = False

    if run_coverage:
        local('rm -rf ' + directory)
        package = __import__('site')
        base_path = dirname(package.__file__) + '/site-packages/' + get_full_name().replace('.', '/')
        print "Coverage is covering: " + base_path
        cov = coverage.coverage(branch=True,
                                source=(base_path,),
                                omit=('*/migrations/*',))
        cov.start()
    yield

    if run_coverage:
        cov.stop()
        cov.html_report(directory=directory)
    else:
        print "Install coverage.py to measure test coverage"


@task
def clean():
    """Find and remove all .pyc and .pyo files"""
    local('find . -name "*.py[co]" -exec rm {} \;')


@task
def create_migration(name, initial=False, auto=True):
    """Create a South migration for app"""
    command((("schemamigration", fabfile.main_app, name), {
        "initial": bool(int(initial)),
        "auto": bool(int(auto)),
    }))


@task
def command(*cmds):
    """Run and arbitrary set of Django commands"""
    runner = VirtualDjango()
    runner.run(fabfile.settings)
    for cmd in cmds:
        if type(cmd) is tuple:
            args, kwargs = cmd
        else:
            args = (cmd, )
            kwargs = {}
        runner.call_command(*args, **kwargs)


@task
def pep8():
    """Run pep8 on all .py files in ./armstrong"""
    local('find ./armstrong -name "*.py" | xargs pep8 --repeat', capture=False)


@task
@pip_install
def test():
    """Run tests against `tested_apps`"""
    from types import FunctionType
    if hasattr(fabfile, 'settings') and type(fabfile.settings) is not FunctionType:
        with html_coverage_report():
            run_django_tests(fabfile.settings, *fabfile.tested_apps)
        return
    else:
        test_module = "%s.tests" % get_full_name()
        try:
            __import__(test_module)
            tests = sys.modules[test_module]
        except ImportError:
            tests = False
            pass

        if tests:
            test_suite = getattr(tests, "suite", False)
            if test_suite:
                with html_coverage_report():
                    unittest.TextTestRunner().run(test_suite)
                return

    raise ImproperlyConfigured(
        "Unable to find tests to run.  Please see armstrong.dev README."
    )


@task
def runserver():
    """Create a Django development server"""
    command("runserver")


@task
def shell():
    """Launch shell with same settings as test and runserver"""
    command("shell")


@task
def syncdb():
    """Call syncdb and migrate on project"""
    command("syncdb", "migrate")


@task
def docs():
    """Generate the Sphinx docs for this project"""
    local("cd docs && make html")


@task
@pip_install
def spec(verbosity=4):
    """Run harvest to run all of the Lettuce specs"""
    defaults = {"DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        },
    }}

    get_full_name()
    defaults.update(fabfile.settings)
    v = VirtualDjango()
    v.run(defaults)
    v.call_command("syncdb", interactive=False)
    v.call_command("migrate")
    v.call_command("harvest", apps=fabfile.full_name,
            verbosity=verbosity)

def get_full_name():
    if not hasattr(fabfile, "full_name"):
        try:
            package_string = local("cat ./package.json", capture=True)
            package_obj = json.loads(package_string)
            fabfile.full_name = package_obj['name']
            return fabfile.full_name
        except:
            sys.stderr.write("\n".join([
                red("No `full_name` variable detected in your fabfile!"),
                red("Please set `full_name` to the app's full module"),
                red("Additionally, we couldn't read name from package.json"),
                ""
            ]))
            sys.stderr.flush()
            sys.exit(1)
    return fabfile.full_name


@task
def reinstall():
    """Install the current component"""
    local("pip uninstall -y `basename \\`pwd\\``; pip install .")
