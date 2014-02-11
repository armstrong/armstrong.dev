import sys
from os.path import dirname
from contextlib import contextmanager

try:
    from invoke import task, run
except ImportError:
    sys.stderr.write("Tasks require Invoke: `pip install invoke`\n")
    sys.exit(1)

# Decorator keeps the function signature and argspec intact, which we
# need so @task can build out CLI arguments properly
from decorator import decorator

from .dev_django import run_django_cmd, run_django_cli, DjangoSettings


__all__ = [
    "clean", "create_migration", "pep8", "managepy",
    "coverage", "test", "install", "remove_armstrong"]


# Grab our package information
import json
package = json.load(open("./package.json"))


HELP_TEXT_MANAGEPY = 'any command that `manage.py` normally takes, including "help"'
HELP_TEXT_EXTRA = 'include any arguments this method can normally take. ' \
    'multiple args need quotes, e.g. --extra "test1 test2 --verbosity=2"'
HELP_TEXT_REPORTS = 'directory to store coverage reports, default: "coverage"'


@decorator
def require_self(func, *args, **kwargs):
    """Decorator to require that this component be installed"""

    try:
        __import__(package['name'])
    except ImportError:
        sys.stderr.write(
            "This component needs to be installed first. Run " +
            "`invoke install`\n")
        sys.exit(1)
    return func(*args, **kwargs)


def require_pip_module(module):
    """Decorator to check for a module and helpfully exit if it's not found"""

    def wrapper(func, *args, **kwargs):
        try:
            __import__(module)
        except ImportError:
            sys.stderr.write(
                "`pip install %s` to enable this feature\n" % module)
            sys.exit(1)
        else:
            return func(*args, **kwargs)
    return decorator(wrapper)


@contextmanager
def html_coverage_report(report_directory=None):
    package_parent = str(package['name'].rsplit('.', 1)[0])  # fromlist can't handle unicode
    module = __import__(package['name'], fromlist=[package_parent])
    base_path = dirname(module.__file__)

    import coverage as coverage_api
    print("Coverage is covering: %s" % base_path)
    cov = coverage_api.coverage(branch=True, source=[base_path])

    cov.start()
    yield
    cov.stop()

    # Write results
    report_directory = report_directory or "coverage"
    run('rm -rf ' + report_directory)
    cov.html_report(directory=report_directory)
    print("Coverage reports available in: %s " % report_directory)


@task
def clean():
    """Find and remove all .pyc and .pyo files"""
    run('find . -name "*.py[co]" -exec rm {} \;')


@task
@require_self
@require_pip_module('south')
def create_migration(initial=False):
    """Create a South migration for this project"""

    settings = DjangoSettings()
    if 'south' not in (name.lower() for name in settings.INSTALLED_APPS):
        print("Temporarily adding 'south' into INSTALLED_APPS.")
        settings.INSTALLED_APPS.append('south')

    kwargs = dict(initial=True) if initial else dict(auto=True)
    run_django_cmd('schemamigration', package['name'], **kwargs)


@task
@require_pip_module('pep8')
def pep8():
    """Run pep8 on all .py files in ./armstrong"""
    run('find ./armstrong -name "*.py" | xargs pep8 --repeat')


@task(help=dict(extra=HELP_TEXT_EXTRA))
@require_self
def test(extra=None):
    """Test this component via `manage.py test`"""
    return managepy('test', extra)


@task(help=dict(reportdir=HELP_TEXT_REPORTS, extra=HELP_TEXT_EXTRA))
@require_self
@require_pip_module('coverage')
def coverage(reportdir=None, extra=None):
    """Test this project with coverage reports"""

    try:
        with html_coverage_report(reportdir):
            return test(extra)
    except (ImportError, EnvironmentError):
        sys.exit(1)


@task(help=dict(cmd=HELP_TEXT_MANAGEPY, extra=HELP_TEXT_EXTRA))
def managepy(cmd, extra=None):
    """Run manage.py using this component's specific Django settings"""

    extra = extra.split() if extra else []
    run_django_cli(['invoke', cmd] + extra)


@task
def install(editable=True):
    """Install this component (or remove and reinstall)"""

    try:
        __import__(package['name'])
    except ImportError:
        pass
    else:
        run("pip uninstall --quiet -y %s" % package['name'], warn=True)

    cmd = "pip install --quiet "
    cmd += "-e ." if editable else "."

    run(cmd, warn=True)


@task
def remove_armstrong():
    """Remove all Armstrong components (except for Dev) from this environment"""

    from pip.util import get_installed_distributions
    pkgs = get_installed_distributions(local_only=True, include_editables=True)
    apps = [pkg for pkg in pkgs
        if pkg.key.startswith('armstrong') and pkg.key != 'armstrong.dev']

    for app in apps:
        run("pip uninstall -y %s" % app.key)

    if apps:
        print(
            "Note: this hasn't removed other dependencies installed by "
            "these components. There's no substitute for a fresh virtualenv.")
    else:
        print("No Armstrong components to remove.")
