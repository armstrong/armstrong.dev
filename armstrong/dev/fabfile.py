import sys
from os.path import dirname
from ast import literal_eval
from functools import wraps
from contextlib import contextmanager

from fabric.api import local, settings
from fabric.colors import yellow, red
from fabric.decorators import task


from armstrong.dev.dev_django import run_django_cmd, DjangoSettings

FABRIC_TASK_MODULE = True

__all__ = ["clean", "create_migration", "pep8", "proxy",
    "coverage", "test", "install", "remove_armstrong"]


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


def require_pip_module(module):
    """Decorator to check for a module and helpfully exit if it's not found"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                __import__(module)
            except ImportError:
                sys.stderr.write(
                    yellow("`pip install %s` to enable this feature\n" % module))
                sys.exit(1)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator


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
    local('rm -rf ' + report_directory)
    cov.html_report(directory=report_directory)
    print("Coverage reports available in: %s " % report_directory)


@task
def clean():
    """Find and remove all .pyc and .pyo files"""
    local('find . -name "*.py[co]" -exec rm {} \;')


@task
@require_self
@require_pip_module('south')
def create_migration(initial=False):
    """Create a South migration for this project"""

    settings = DjangoSettings()
    if 'south' not in (name.lower() for name in settings.INSTALLED_APPS):
        print("Temporarily adding 'south' into INSTALLED_APPS.")
        settings.INSTALLED_APPS.append('south')

    kwargs = dict(initial=True) if literal_eval(str(initial)) else dict(auto=True)
    run_django_cmd('schemamigration', package['name'], **kwargs)


@task
@require_pip_module('pep8')
def pep8():
    """Run pep8 on all .py files in ./armstrong"""
    local('find ./armstrong -name "*.py" | xargs pep8 --repeat', capture=False)


@task
@require_self
def test(*args, **kwargs):
    """Test this component via `manage.py test`"""
    run_django_cmd('test', *args, **kwargs)


@task
@require_self
@require_pip_module('coverage')
def coverage(*args, **kwargs):
    """Test this project with coverage reports"""

    # Option to pass in the coverage report directory
    coverage_dir = kwargs.pop('coverage_dir', None)

    try:
        with html_coverage_report(coverage_dir):
            run_django_cmd('test', *args, **kwargs)
    except (ImportError, EnvironmentError):
        sys.exit(1)


@task
def proxy(cmd=None, *args, **kwargs):
    """Run manage.py using this component's specific Django settings"""

    if cmd is None:
        sys.stderr.write(red("Usage: fab proxy:<command>,arg1,kwarg=1\n") +
            "which translates to: manage.py command arg1 --kwarg=1\n")
        sys.exit(1)
    run_django_cmd(cmd, *args, **kwargs)


@task
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
    cmd += "-e ." if literal_eval(str(editable)) else "."

    with settings(warn_only=True):
        local(cmd, capture=False)


@task
def remove_armstrong():
    """Remove all armstrong components (except for dev) from this environment"""

    from pip.util import get_installed_distributions
    pkgs = get_installed_distributions(local_only=True, include_editables=True)
    apps = [pkg for pkg in pkgs
        if pkg.key.startswith('armstrong') and pkg.key != 'armstrong.dev']

    for app in apps:
        local("pip uninstall -y %s" % app.key)

    if apps:
        print("Note: this hasn't removed other dependencies installed by "
            "these components. There's no substitute for a fresh virtualenv.")
    else:
        print("No armstrong components to remove.")
