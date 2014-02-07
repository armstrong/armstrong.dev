armstrong.dev
=============
Tools and such for handling development of Armstrong applications

This package contains some of the various helpers needed to do development work
on the Armstrong packages.  If you're not actively developing, or working with
development versions of Armstrong, you probably don't need this package.

Installation
------------
1. ``pip install armstrong.dev``


Usage
-----
Most Armstrong components already have the necessary configuration to use these
Dev tools. Type ``invoke --list`` to see a list of all of the commands.

If you are creating a new component (or perhaps updating one that uses
the older, pre 2.0 Dev tools), you'll need these next two steps.

1. Create a ``tasks.py`` and add the following::

    from armstrong.dev.tasks import *

    # any additional Invoke commands
    # ...

2. Create an ``env_settings.py`` and add the following::

    from armstrong.dev.default_settings import *

    # any additional settings
    # ...


Notable changes in 2.0
----------------------
This version offers an easier and more standard way to run a Django
environment with a component's specific settings, either from the
commandline or via import.

It provides an "a la carte" requirements approach. Meaning that if you run an
Invoke command that needs a package that isn't installed, it will prompt you
to install it instead of requiring everything up-front. This allows for much
faster virtualenv creation (which saves considerable time in testing) and
doesn't pollute your virtualenv with packages for features you don't use.

``test`` and ``coverage`` will work better with automated test tools like
TravisCI and Tox.::

	invoke test

Settings are now defined in the normal Django style in an ``env_settings.py``
file instead of as a dict within the tasks file. It's not called "settings.py"
to make it clearer that these are settings for the development and testing
of this component, not necessarily values to copy/paste for incorporating
the component into other projects.


Backward incompatible changes in 2.0
------------------------------------
* ``env_settings.py`` is necessary and contains the settings that
  ``tasks.py`` used to have.

* ``tasks.py`` imports from a different place and no longer defines the
  settings configurations.

Not required but as long as you are reviewing the general state of things,
take care of these things too!

* Review the ``requirements`` files.
* Add a ``tox.ini`` file.
* Review or add a TravisCI configuration.
* Review ``.gitignore``. You might want to ignore these::

	.tox/
	coverage*/
	*.egg-info


Contributing
------------

* Create something awesome -- make the code better, add some functionality,
  whatever (this is the hardest part).
* `Fork it`_
* Create a topic branch to house your changes
* Get all of your commits in the new topic branch
* Submit a `Pull Request`_

.. _Pull Request: https://help.github.com/articles/using-pull-requests
.. _Fork it: https://help.github.com/articles/fork-a-repo


State of Project
----------------
Armstrong is an open-source news platform that is freely available to any
organization.  It is the result of a collaboration between the `Texas Tribune`_
and `The Center for Investigative Reporting`_ and a grant from the
`John S. and James L. Knight Foundation`_.

To follow development, be sure to join the `Google Group`_.

``armstrong.dev`` is part of the `Armstrong`_ project. You're
probably looking for that.


.. _Armstrong: http://www.armstrongcms.org/
.. _The Center for Investigative Reporting: http://cironline.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
.. _Texas Tribune: http://www.texastribune.org/
.. _Google Group: http://groups.google.com/group/armstrongcms
