import pkg_resources
pkg_resources.declare_namespace(__name__)


from contextlib import contextmanager
try:
    import coverage
except ImportError:
    coverage = False
import os
from os.path import basename, dirname
import sys

from fabric.api import *
from fabric.decorators import task

if not "fabfile" in sys.modules:
    sys.stderr.write("This expects to have a 'fabfile' module\n")
    sys.stderr.write(-1)
fabfile = sys.modules["fabfile"]


try:
    from d51.django.virtualenv.test_runner import run_tests
except ImportError, e:
    sys.stderr.write(
            "This project requires d51.django.virtualenv.test_runner\n")
    sys.exit(-1)


FABRIC_TASK_MODULE = True


__all__ = ["clean", "command", "create_migration", "pep8", "test", "runserver",
           "shell", "syncdb", ]

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
    from d51.django.virtualenv.base import VirtualEnvironment
    runner = VirtualEnvironment()
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
