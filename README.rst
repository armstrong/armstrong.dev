armstrong.dev
=============

.. image:: https://img.shields.io/pypi/v/armstrong.dev.svg
  :target: https://pypi.python.org/pypi/armstrong.dev/
  :alt: PyPI Version
.. image:: https://img.shields.io/pypi/l/armstrong.dev.svg
  :target: https://pypi.python.org/pypi/armstrong.dev/
  :alt: License

Tools and such for handling development of Armstrong applications

This package contains some of the various helpers needed to do development work
on the Armstrong packages. If you're not actively developing, or working with
development versions of Armstrong, you probably don't need this package.


Installation & Configuration
----------------------------
If you are just running tests for a component, Tox will grab everything it
needs including ArmDev.

- ``pip install tox`` and run ``tox``

Otherwise:

- ``pip install armstrong.dev invoke``

`Invoke`_ is not strictly required. ArmDev is as lean as possible to support
fast virtualenv creation so multi-environment testing tools like TravisCI
and Tox will complete ASAP.

Many of the Invoke tasks have their own package requirements and they will
nicely notify you if something they require needs to be installed.

This component supports Django 1.3, 1.4, 1.5, 1.6, 1.7 on Python 2.6 and 2.7.


.. _Invoke: http://docs.pyinvoke.org/en/latest/index.html


Usage
-----
Most Armstrong components already have the necessary configuration to use these
Dev tools. Specifically, components need ``tasks.py`` and ``env_settings.py``
files. Assuming these are present:

``invoke --list``
  to see a list of all available commands

``invoke --help <cmd>``
  for help on a specific command

Several of the tasks take an optional ``--extra`` argument that is used as a
catch-all way of passing arbitrary arguments to the underlying command. Invoke
cannot handle arbitrary args (like Fabric 1.x could) so this is our workaround.
Two general rules: 1) enclose multiple args in quotes 2) kwargs need to use
"=" with no spaces (our limitation, not Invoke's). Example:
``invoke test --extra "--verbosity=2 <path.to.app.test1> <path.to.app.test2>"``

``invoke install [--editable]``
  to "pip install" the component, by default as an `editable`_ install. For
  a regular install, use ``--no-editable`` or ``--editable=False``.

``invoke test [--extra ...]``
  to run tests where --extra handles anything the normal Django
  "manage.py test" command accepts.

``invoke coverage [--reportdir=<directory>] [--extra ...]``
  for running test coverage. --extra works the same as in "invoke test" passing
  arbitrary args to the underlying test command. --reportdir is where the HTML
  report will be created; by default this directory is named "htmlcov" or
  whatever is set in the ``.coveragerc`` file.

``invoke managepy <cmd> [--extra ...]``
  to run any Django "manage.py" command where --extra handles any arbitrary
  args. Example: ``invoke managepy shell`` or
  ``invoke managepy runserver --extra 9001``

``invoke create_migration [--initial]``
  to create a South migration for the component (in Django <1.7).
  An "auto" migration is default if the --initial flag is not used.

There are other commands as well, but these are the most useful. Remember
that individual components may provide additional Invoke tasks as well. So
run ``invoke --list`` to discover them all.


.. _editable: http://pip.readthedocs.org/en/latest/reference/pip_install.html#editable-installs


Component Setup
---------------
If you are creating a new Armstrong component or updating one that uses the
pre-2.0 ArmDev, you'll need to create (or port to) these two files:

1. Create a ``tasks.py`` and add the following::

    from armstrong.dev.tasks import *

    # any additional Invoke commands
    # ...

2. Create an ``env_settings.py`` and add the following::

    from armstrong.dev.default_settings import *

    # any additional settings
    # it's likely you'll need to extend the list of INSTALLED_APPS
    # ...

Not required but as long as you are reviewing the general state of things,
take care of these too!

- Review the ``requirements`` files
- Review the TravisCI configuration
- Drop Lettuce tests and requirements
- Add a ``tox.ini`` file
- Review the README text and setup.py metadata
- Use Setuptools and fix any improper namespacing
- Stop shipping tests by moving tests/ to the root directory
- If the component uses logging, consider namespacing it with
  ``logger = logging.getLogger(__name__)``.
- Add a ``CHANGES.rst`` file and include it in the MANIFEST
- Review ``.gitignore``. You might want to ignore these::

	.tox/
	coverage*/
	*.egg-info


Notable changes in 2.0
----------------------
Setuptools is now explicitly used/required instead of Distutils.

Invoke replaces Fabric for a leaner install without the SSH and crypto
stuff. Invoke is still pre-1.0 release so we might have some adjustment
to do later.

This version offers an easier and more standard way to run a Django
environment with a component's specific settings, either from the
commandline or via import.

It provides an "a la carte" requirements approach. Meaning that if you run an
Invoke command that needs a package that isn't installed, it will prompt you
to install it instead of requiring everything up-front. This allows for much
faster virtualenv creation (which saves considerable time in testing) and
doesn't pollute your virtualenv with packages for features you don't use.

``test`` and ``coverage`` will work better with automated test tools like
TravisCI and Tox. These commands also now work like Django's native test
command so that you can pass arguments for running selective tests or
changing the output verbosity.

Settings are now defined in the normal Django style in an ``env_settings.py``
file instead of as a dict within the tasks file. It's not called "settings.py"
to make it clearer that these are settings for the development and testing
of this component, not necessarily values to copy/paste for incorporating
the component into other projects.

The full list of changes and backward incompatibilties is available
in **CHANGES.rst**.


Contributing
------------
Development occurs on Github. Participation is welcome!

* Found a bug? File it on `Github Issues`_. Include as much detail as you
  can and make sure to list the specific component since we use a centralized,
  project-wide issue tracker.
* Have code to submit? Fork the repo, consolidate your changes on a topic
  branch and create a `pull request`_.
* Questions, need help, discussion? Use our `Google Group`_ mailing list.

.. _Github Issues: https://github.com/armstrong/armstrong/issues
.. _pull request: http://help.github.com/pull-requests/
.. _Google Group: http://groups.google.com/group/armstrongcms


State of Project
----------------
`Armstrong`_ is an open-source news platform that is freely available to any
organization. It is the result of a collaboration between the `Texas Tribune`_
and `The Center for Investigative Reporting`_ and a grant from the
`John S. and James L. Knight Foundation`_. Armstrong is available as a
complete bundle and as individual, stand-alone components.

.. _Armstrong: http://www.armstrongcms.org/
.. _Texas Tribune: http://www.texastribune.org/
.. _The Center for Investigative Reporting: http://cironline.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
