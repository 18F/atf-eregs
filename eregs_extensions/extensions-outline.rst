eRegulations Parser Extensions Outline
======================================
eRegulations has three main projects:

+   `regulations-core`_.
+   `regulations-parser`_.
+   `regulations-site`_.

The current approach to developing for a new agency is to have an umbrella project that pulls in `regulations-core`_ and `regulations-site`_ via ``pip install``, and that overrides HTML and CSS elements of `regulations-site`_. An example of that approach is `atf-eregs`_.

This document is concerned with extensions to `regulations-parser`_, which are handled differently.

We assume that the above umbrella approach will be followed, and that an umbrella project of some kind is present and loaded as a set of Python packages via the umbrella project's ``setup.py`` file, and that the developer also has `regulations-parser`_ in their environment and is running it to test changes.

A common setup might look like this::

    cd <project-root>
    git clone https://github.com/18F/atf-eregs
    git clone https://github.com/18F/regulations-parser
    cd atf-eregs
    pip install -r requirements.txt
    cd ../regulations-parser
    pip install -r requirements.txt
    pip install -r requirements_test.txt

The umbrella project, in this case ``atf-eregs``, has a directory in it named ``eregs_extensions``. This is where agency-specific `regulations-parser`_ code lives.

Namespaces and Modules
----------------------
In ``eregs_extensions`` is a directory named ``atf_regparser``. This directory name determines the name of the Python module that will be pulled in by `regulations-parser`_, and must be renamed to something unique to the agency using the extensions. This name must also match the value of the ``fs`` variable in ``eregs_extensions/setup.py``.

`regulations-parser`_ uses `stevedore`_ to handle bringing in modules, determined by their entry points, which we use as namespaces.

The `regulations-parser`_ namespace prefix is ``eregs_ns.parser``, and the parser will only look for extensions whose declared entry points match that.

Currently, the only supported namespaces are ``eregs_ns.parser.preprocessors`` and ``eregs_ns.parser.test_suite``. In future, we hope to have all new agency-specific features use the extensions system, and to add new hooks to `regulations-parser`_ to find extensions in the appropriate code paths.

Creating a New Preprocessor
---------------------------
Let's say we have a new agency, MIB, who wish to use eRegulations and to make additions to `regulations-parser`_ to handle their regulations. They fork https://github.com/18F/atf-eregs as ``mib-eregs`` and then follow the setup above.

In ``mib-eregs``, the first thing they would do is rename the ``atf_regparser`` directory to ``mib_regparser``, and alter the ``setup.py`` file so that::

    fs = "atf_regparser"  # The directory name for the package.

becomes::

    fs = "mib_regparser"  # The directory name for the package.

They would remove the existing ATF-specific preprocessors from ``eregs_extensions/mib_regparser/preprocs``, and do the same for the contents of ``eregs_extensions/mib_regparser/tests``.

Any new preprocessor would need to import the base class::

    from regparser.tree.xml_parser.preprocessors import PreProcessorBase

And would likely need ``etree``::

    from lxml import etree

They would also need tests. The tests would need the following import lines::

    from unittest import TestCase
    from regparser.test_utils.xml_builder import XMLBuilder
    from mib_regparser.preprocs import <whatever the test is for>

Note that the test has to reflect the filesystem name ``mib_regparser``—in other words, each test has to change if that name changes.

Current Extension Hooks
-----------------------
In `regulations-parser`_, ``settings.py`` creates a list of preprocessors and then looks for extensions to add to that list using `stevedore`_::

    try:
        stevedore_mgr = extension.ExtensionManager(
            namespace="eregs_ns.parser.preprocessors", invoke_on_load=False)
        stevedore_mgr.map(lambda ext: PREPROCESSORS.append(ext.entry_point_target))
    except NoMatches:
        pass

Both ``regparser/tree/xml_parser/xml_wrapper.py`` and ``regparser/builder.py`` import ``regparser/tree/xml_parser/extended_preprocessors.py``, which iterates through that list of preprocessors and imports the modules, and returns a list of them to be used.

``regparser/commands/full_tests.py`` looks for extensions in the ``eregs_ns.parser.test_suite`` namespace and runs those in addition to `regulations-parser`_'s own tests.

Future Extension Hooks
----------------------
A non-comprehensive list of other hooks we might add and what their namespaces would be:

``ParagraphProcessors``
    ``eregs_ns.parser.paragraph_processors``
``Matchers``
    ``eregs_ns.parser.matchers``
Subtree Processors
    ``eregs_ns.parser.subtree_processors``
Tree Builders
    ``eregs_ns.parser.tree_builders``
``AppendixProcessors``
    ``eregs_ns.parser.appendix_processors``


.. _regulations-core: https://github.com/18F/regulations-core
.. _regulations-parser: https://github.com/18F/regulations-parser
.. _regulations-site: https://github.com/18F/regulations-site
.. _atf-eregs: https://github.com/18F/atf-eregs
.. _stevedore: http://docs.openstack.org/developer/stevedore/
