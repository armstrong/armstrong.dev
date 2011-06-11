armstrong.dev
=============
Tools and such for handling development of Armstrong applications

This package contains some of the various helpers needed to do development work
on the Armstrong packages.  If you're not actively developing, or working with
development versions of Armstrong, you probably don't need this package.

Usage
-----

Create a `fabfile` (either `fabfile/__init__.py` or simply `fabfile.py`) in
your project and add the following::

    from armstrong.dev.tasks import *


    settings = {
        "DEBUG": True,
        # And so on with the keys being the name of the setting and the values
        # the appropriate value.
    }

    main_app = "name.of.your.app"
    tested_apps ("another_app", main_app, )


Now your fabfile will expose the various commands for setting up and running
your reusable app inside a virtualenv for testing, interacting with via the
shell, and even running a simple server.

Type ``fab -l`` to see a list of all of the commands.


Installation
------------

::

    name="armstrong.dev"
    pip install -e git://github.com/armstrong/$name#egg=$name

**Note**: This currently relies on a development version of Fabric.  This
requirement is set to be dropped once Fabric 1.1 is released.  To ensure this
runs as expected, install the ``tswicegood/fabric`` fork of Fabric:

::

    pip install -e git://github.com/tswicegood/fabric.git#egg=fabric


Contributing
------------

* Create something awesome -- make the code better, add some functionality,
  whatever (this is the hardest part).
* `Fork it`_
* Create a topic branch to house your changes
* Get all of your commits in the new topic branch
* Submit a `pull request`_


License
-------
Copyright 2011 Bay Citizen and Texas Tribune

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. _pull request: http://help.github.com/pull-requests/
.. _Fork it: http://help.github.com/forking/
