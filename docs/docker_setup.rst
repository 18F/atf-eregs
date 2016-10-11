============
Docker Setup
============

If you want to get started with minimal fuss and aren't interested in much
development, you may want to try getting set up with Docker. This approach
will give you an ATF-eRegs instance running in development mode without
needing to set up Python, Node, etc.

You will need to first install `Docker 
<https://www.docker.com/products/overview>`_. This will generally install
`Docker Compose <https://docs.docker.com/compose/install/>`_, but you will
need that as well if not. You'll also need to `clone 
<https://help.github.com/articles/cloning-a-repository/>`_ the ATF-eRegs
repository and then run Docker Compose:

.. code-block:: bash

  git clone https://github.com/18F/atf-eregs.git
  cd atf-eregs
  docker-compose up

This a great deal of time, depending on your hardware. Once it's all done,
navigate your browser to `http://0.0.0.0:8080/ <http://0.0.0.0:8080/>`_.
