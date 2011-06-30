
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)


from contextlib import contextmanager
try:
    import coverage
except ImportError:
    coverage = False
import os
from os.path import basename, dirname
import sys
from functools import wraps

import json

from fabric.api import *
from fabric.colors import red
from fabric.decorators import task

from armstrong.dev.virtualdjango.test_runner import run_tests
from armstrong.dev.virtualdjango.base import VirtualDjango

if not "fabfile" in sys.modules:
    sys.stderr.write("This expects to have a 'fabfile' module\n")
    sys.stderr.write(-1)
fabfile = sys.modules["fabfile"]


FABRIC_TASK_MODULE = True


__all__ = ["clean", "command", "create_migration", "docs", "pep8", "test",
           "runserver", "shell", "spec", "syncdb", ]


def possibly_pip_install(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if getattr(fabfile, "pip_install_first", True):
            with settings(warn_only=True):
                local("pip uninstall -y %s" % get_full_name(), capture=False)
                local("pip install --no-deps .", capture=False)
        func(*args, **kwargs)
    return inner


@contextmanager
def html_coverage_report(directory="./coverage"):
    # This relies on this being run from within a directory named the same as
    # the repository on GitHub.  It's fragile, but for our purposes, it works.
    if coverage:
        base_path = os.path.join(dirname(dirname(__file__)), "armstrong")
        files_to_cover = []
        for (dir, dirs, files) in os.walk(base_path):
            if not dir.find("tests") is -1:
                continue
            valid = lambda a: a[0] != "." and a[-3:] == ".py"
            files_to_cover += ["%s/%s" % (dir, file) for file in files if valid(file)]
        cov = coverage.coverage(branch=True, include=files_to_cover)
        cov.start()
    yield

    if coverage:
        cov.stop()
        cov.html_report(directory=directory)
    else:
        print "Install coverage.py to measure test coverage"


@task
def clean():
    """Find and remove all .pyc and .pyo files"""
    local('find . -name "*.py[co]" -exec rm {} \;')


@task
def create_migration(name):
    """Create a migration for provided app -- requires South"""
    command((("schemamigration", fabfile.main_app, name), {"initial": True}))


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
    local('find ./armstrong -name "*.py" | xargs pep8', capture=False)


@task
@possibly_pip_install
def test():
    """Run tests against `tested_apps`"""
    with html_coverage_report():
        run_tests(fabfile.settings, *fabfile.tested_apps)


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
@possibly_pip_install
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