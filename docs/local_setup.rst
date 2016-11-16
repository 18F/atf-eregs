===========
Local Setup
===========

Note that for the quickest setup, you may want to consider our
:doc:`docker_setup` instructions.

This application requires Python 2.7. `Install it (if you haven't already)
<http://docs.python-guide.org/en/latest/starting/installation/>`_, `set up a
virtualenv for this project and activate it
<http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ (using Python
2.7), and then `clone this repository
<https://help.github.com/articles/cloning-a-repository/>`_. Throughout these
docs, we'll assume you are running in a \*nix environment (Linux, BSD, OS X,
etc.); Windows instructions would be similar.

Executing

.. code-block:: bash

  python --version

should return something like

.. code-block:: bash

  Python 2.7.10+

Next, we need to install all of the appropriate requirements (including the
other components of eRegs). We'll assume you have `pip
<https://pip.pypa.io/en/stable/installing/>`_ and `Node.JS & npm
<https://nodejs.org/en/download/>`_ installed.

.. code-block:: bash

  npm install -g grunt-cli bower
  pip install -r requirements.txt

Then initialize the database (SQLite by default; see `Production`) and build
the frontend:

.. code-block:: bash

  python manage.py migrate --fake-initial
  python manage.py compile_frontend

Then select one of the two setup options in the :ref:`Data` section. After that, you can run a
development server locally via

.. code-block:: bash

  python manage.py runserver

.. _data:

Data
====
For an instance of ATF-eRegs to display regulations data, it needs to have
access to said data. There are two basic schemes to set this up -- you can
either point your checkout to `existing` parsed regulations (ideal for folks
only working on the front-end or who want to see a UI quickly), or you can
`populate` your database with parsed regulations.

Point to Existing Data
----------------------

In this scenario, we just need to configure the UI to point to the live API:

.. code-block:: bash

  echo "API_BASE = 'https://atf-eregs.app.cloud.gov/api/'" >> local_settings.py

Parsing Regulations
-------------------

To parse ATF's regulations, you will need to *also* install the parsing
library.

.. code-block:: bash

  pip install git+https://github.com/eregs/regulations-parser.git@4.0.0#egg=regparser

Then, you will want to start your local server and send it the parsed data.
These steps will take several minutes.

.. code-block:: bash

  python manage.py runserver &    # start the server as a background process
  # Set up the parser's database
  python manage.py migrate --settings=regparser.web.settings.dev
  eregs pipeline 27 447 http://localhost:8000/api   # send the data for one reg
  eregs pipeline 27 478 http://localhost:8000/api
  eregs pipeline 27 479 http://localhost:8000/api
  eregs pipeline 27 555 http://localhost:8000/api
  eregs pipeline 27 646 http://localhost:8000/api

Then navigate to http://localhost:8000

Editable Libraries
==================

Though this repository (atf-eregs) contains all of the ATF-specific code, you
will most likely want to extend functionality in the base libraries as well.
To do this, fork and check out the appropriate library (`regulations-site <https://github.com/18F/regulations-site>`_,
`regulations-core <https://github.com/18F/regulations-core>`_,
`regulations-parser <https://github.com/18F/regulations-parser>`_) into a
separate directory, then install it via

.. code-block:: bash

  pip install -e /path/to/that/checkout

This will tell Python to use your local version of that library rather than
the upstream version. Although the Python and templates will change as soon
as you modify them in the -site checkout, you will need to run
`compile_frontend` (see above) to integrate stylesheet and JS changes.

Fixing Errors
==================

If you pulled down the latest code changes, ran the server locally, and something didn't build correctly (you got an error message instead of seeing eRegulations), try running standard updates:

For any component that you're working with (including atf-eregs), first do ``pip install -r requirements.txt`` to update the requirements.

If working with the parser, do ``eregs clear``.

Or if working with atf-eregs, do ``python manage.py compile_frontend`` to compile the frontend.

And then try running the server again.

Gotchas
=======

Ports
-----
For the time being, this application, which cobbles together
`regulations-core <https://github.com/18F/regulations-core>`_ and
`regulations-site <https://github.com/18F/regulations-site>`_, makes HTTP
calls to itself. The server therefore needs to know which port it is set up to
listen on.

We default to 8000, as that's the standard for django's ``runserver``, but if
you need to run on a different port, use:

.. code-block:: bash

    python manage.py runserver 1234

You will also have to either export an environmental variable or create a
``local_settings.py`` file as follows:

.. code-block:: bash

  export PORT=1234

OR

.. code-block:: bash

  echo "API_BASE = 'http://localhost:1234/api/'" >> local_settings.py
