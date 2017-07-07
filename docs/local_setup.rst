====================
Local (Docker) Setup
====================

We develop using `Docker
<https://www.docker.com/products/overview#install_the_platform>`_, an open
source container engine. If you haven't already please install Docker and
`Docker-compose <https://docs.docker.com/compose/install/>`_ (which is
installed automatically with Docker on Windows and OS X).

To get started, you will need to `clone
<https://help.github.com/articles/cloning-a-repository/>`_ the ATF-eRegs
repository, build the frontend, and run the app:

.. code-block:: bash

  git clone https://github.com/18F/atf-eregs.git
  cd atf-eregs
  ./devops/compile_frontend.sh build-dist   # Must be run after CSS edits
  docker-compose up prod

Once that's done, visit the app at `http://0.0.0.0:9000/
<http://0.0.0.0:9000/>`_.


Dev Mode
========

We also can run in "dev" mode, which includes the Django ``DEBUG`` flag and
checks out locally-editable versions of ``regulations-site`` and
``regulations-core``. Run

.. code-block:: bash

  docker-compose up dev

to see this in action. The locally-editable versions of the eregs libraries
can be found in the ``eregs_libs`` directory, should you need to work on the
core code base at the same time as the ATF code base. Note that for the time
being, ``compile_frontend`` shell script *always* uses the local version of
-site when building scripts. Remember to make a pull request for those
upstream changes!


Parsing
=======

When using the  ``dev`` and ``prod`` applications, we're pointing to the
existing, live data. This is helpful to get running quickly, but if we need to
test parsing, we need a local database.

To get that set up and kick off parsing, run

.. code-block:: bash

  ./devops/import_data.sh   # parses regulations, imports them locally
  # later, if we just want to see that data
  docker-compose up dev-with-db

And then visit `http://0.0.0.0:8001/ <http://0.0.0.0:8001/>`_.

The process checks out a copy of ``regulations-parser`` in
``eregs_extensions/eregs_libs/`` which can be further edited (similar to -site
and -core).


Other Tasks
===========

Additionally, you can run containerized versions of several Python and Node
commands:

- ``docker-compose run --rm manage.py`` - the Django management command
- ``docker-compose run --rm py.test`` - our Python test runner
- ``docker-compose run --rm flake8`` - a linter for Python
- ``docker-compose run --rm pip-compile`` - a version-pinning program for
  Python
- ``docker-compose run --rm grunt`` - our JavaScript task runner. See
  `regulations-site <https://github.com/eregs/regulations-site>`_ for more
  details.

Within the ``eregs_extensions`` directory, we can similarly run
``pip-compile``, ``py.test``, and ``flake8`` for just the parser extension.
