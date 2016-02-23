=========
Documentation Updates
=========

These pages are hosted on Read the Docs, a site that automatically (and for free) provides a formatted display of the documentation files stored in `the ATF eRegulations GitHub repository <https://github.com/18F/atf-eregs>`_ in the docs directory (in the master branch).

These files are written in `reStructuredText <http://www.sphinx-doc.org/en/stable/rest.html>`_, a markup language. 

To update these pages: you can edit these files, run the documentation builder (see below), check the generated HTML files to see if they look good, then push the result to the repository. The Read the Docs site will then automatically generate its own HTML files and update these pages.

Build the Docs
==========================

For most edits, you will just need to run the Sphinx documentation
builder again.

.. code-block:: bash

  pip install Sphinx
  cd docs
  make dirhtml

The output will be in ``docs/_build/dirhtml``.

If you are adding new modules, you may need to re-run the skeleton build
script first:

.. code-block:: bash

  pip install Sphinx
  sphinx-apidoc -F -o docs regparser/