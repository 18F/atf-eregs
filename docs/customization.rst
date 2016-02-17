=============
Customization
=============

ATF's eRegs instance consists of several shared (across multiple eRegs
instances) libraries and ATF-specific customizations. Here we will document
these ATF-specific features, deferring to the
`eRegs docs <https://eregs.github.io/>`_ for more broad descriptions around
agency-specific customizations (such as a full list of eRegs' extension
points).

Landing Pages
=============
Each of ATF's regulations have custom landing page content which is tied to
that CFR part. This content is defined in Django's templating language, having
a mix of raw HTML and templating tags. For examples, see five templates
of the form ``atf_eregs/templates/regulations/landing_???.html``; each contain
``blocks`` of content which get merged into appropriate locations within a
larger template. Modifying the content in these files will modify the
corresponding landing page.

Each of the landing pages derive content from
``atf_eregs/templates/regulations/generic_landing.html``, which defines the
shared legal disclaimer.

See Django's
`documentation <https://docs.djangoproject.com/en/1.9/topics/templates/#the-django-template-language>`_
on the subject for an introduction and comprehensive reference guide.

Tags
----
While raw HTML will always work, we strongly recommend using Django's
templating tags to limit the number of edits needed. Notably, review the
existing landing pages for examples of

* ``url`` - dynamically links to another part of eRegs
* ``external_link`` - includes aria labeling and visual indicators that this
  link will open in a new tab
* ``search_for`` - generate a link to search results

Variables
---------
Several variables are available for use within your landing page templates.
Here we document a few of the more useful.

* ``current_version`` - a data structure which includes fields corresponding
  to the unique version identifier for the current (i.e. effective now)
  version of the regulation
* ``new_version`` - a data structure including information about `upcoming`
  versions of this regulation
* ``reg_first_section`` - not all regulations start at section 1
* ``reg_part`` - the CFR part of this regulation
* ``meta`` - a data structure containing meta information about this
  regulation (e.g. its letter, CFR title, etc.)

Branded Templates
=================
The header and footer of each page have been lightly customized to tie in with
ATF's branding. This includes linking to other ATF sites and including ATF's
logo. If the content here needs to be modified for whatever reason,
investigate ``atf_eregs/templates/regulations/favicon.html``,
``full_footer.html``, ``logo.html``, etc. Similarly, ``about.html`` defines
all of the content present on the "About" page.

eRegs supports customized templates primarily through `overriding`. A base set
of templates are provided, broken into components we expect agencies would
need to replace. Creating a file of the same name in the
``atf_eregs/templates/regulations/`` folder effectively `replaces` the
template present in the "core" library. This is somewhat risky, as said
template might be renamed/moved at a later date (though we strive for
backwards compatibility). As such, we recommend only replacing templates on
the periphery of functionality (e.g. footers, headers, etc.). For a full list
of templates, consult the
`regulations-site <https://github.com/18F/regulations-site>`_ project.

Posters
=======
The core eRegs application allows the templates used to render specific
paragraphs/subparagraphs to be replaced on an ad hoc basis. This mechanism is
used to render ATF's "posters" in 27 CFR 478.103, which contain a header
linking to a specific document.

Custom templates of this sort must follow a specific naming convention; they
must be in the ``atf_eregs/templates/regulations/custom_nodes/`` directory and
must be named according to the paragraph they seek to replace. For example,
``478-103-b.html`` will replace the template normally used to render 27 CFR
478.103(b). Consult the ``regulations-site`` documentation for more details.

Style Sheets
============
The core eRegs libraries provide a relatively clean set of stylesheets for
displaying regulations. To integrate with ATF's branding, however, these
style sheets are modified to use the appropriate colors, fonts, and the like.
Similar to the template overriding process, there exist several LESS
components which can be completely replaced by corresponding files in the
``atf_eregs/static/regulations/css/less`` directory. Consult the
``regulations-site`` documentation for full details, but three files are
particularly important.

* ``variables.less`` defines common variables used throughout other less
  files. These largely consist of color schemes
* ``custom-mixins.less`` these mixins are used to override font-families, text
  sizes and the like.
* ``module/custom.less`` this file exists specifically for ATF-specific
  modules, such as style sheets related to Posters.

After making edits to any of these files, remember to run

.. code-block:: bash

  python manage.py compile_frontend

to compile your changes into CSS.
