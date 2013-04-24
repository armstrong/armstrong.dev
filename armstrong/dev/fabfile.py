import sys
from os.path import dirname
from ast import literal_eval
from functools import wraps
from contextlib import contextmanager

from fabric.api import local, settings
from fabric.colors import yellow, red
from fabric.decorators import task

from armstrong.dev.dev_django import run_django_cmd


FABRIC_TASK_MODULE = True

# Grab our package information
import json
package = json.load(open("./package.json"))


def require_self(func=None):
    """Decorator to require that this component be installed"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                __import__(package['name'])
            except ImportError:
                sys.stderr.write(
                    red("This component needs to be installed first. Run ") +
                    yellow("`fab install`\n"))
                sys.exit(1)
            return func(*args, **kwargs)
        return wrapper
    return decorator if not func else decorator(func)



__all__ = ["clean", "create_migration", "docs", "pep8", "test",
           "install", "spec", "proxy"]




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
@require_self
def create_migration(name, initial=False, auto=True):
    """Create a South migration for app"""
    command((("schemamigration", fabfile.main_app, name), {
        "initial": bool(int(initial)),
        "auto": bool(int(auto)),
    }))




@task
def pep8():
    """Run pep8 on all .py files in ./armstrong"""
    local('find ./armstrong -name "*.py" | xargs pep8 --repeat', capture=False)


@task
@require_self
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


@task
def proxy(cmd=None, *args, **kwargs):
    """Run manage.py using this component's specific Django settings"""

    if cmd is None:
        sys.stderr.write(red("Usage: fab proxy:<command>,arg1,kwarg=1\n") +
            "which translates to: manage.py command arg1 --kwarg=1\n")
        sys.exit(1)
    run_django_cmd(cmd, *args, **kwargs)


@task
def docs():
    """Generate the Sphinx docs for this project"""
    local("cd docs && make html")


@task
@require_self
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
def install(editable=True):
    """Install this component (or remove and reinstall)"""

    try:
        __import__(package['name'])
    except ImportError:
        pass
    else:
        with settings(warn_only=True):
            local("pip uninstall --quiet -y %s" % package['name'], capture=False)

    cmd = "pip install --quiet "
    cmd += "-e ." if literal_eval(editable) else "."

    with settings(warn_only=True):
        local(cmd, capture=False)


@task
