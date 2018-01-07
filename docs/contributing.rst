##########################
Contributing to NeoJsonRPC
##########################

Here are some simple rules & tips to help you contribute to NeoJsonRPC. You can contribute in many
ways!

Contributing code
=================

The preferred way to contribute to NeoJsonRPC is to submit pull requests to the `project's Github
repository <https://github.com/ellmetha/neojsonrpc>`_. Here are some general tips regarding pull
requests.

Development environment
-----------------------

.. note::

    The following steps assumes you have `Pipenv <https://docs.pipenv.org/>`_ installed on your
    system.

You should first fork the `NeoJsonRpc's repository <https://github.com/ellmetha/neojsonrpc>`_. Then
you can get a working copy of the project using the following commands:

.. code-block:: bash

  $ git clone git@github.com:<username>/neojsonrpc.git
  $ cd neojsonrpc
  $ make

Coding style
############

Please make sure that your code is compliant with the
`PEP8 style guide <https://www.python.org/dev/peps/pep-0008/>`_. You can ignore the "Maximum Line
Length" requirement but the length of your lines should not exceed 100 characters. Remember that
your code will be checked using `flake8 <https://pypi.python.org/pypi/flake8>`_ and
`isort <https://pypi.python.org/pypi/isort/4.2.5>`_. You can use the following command to trigger
such quality assurance checks:

.. code-block:: bash

  $ make qa

Tests
#####

You should not submit pull requests without providing tests. NeoJsonRPC relies on
`pytest <http://pytest.org/latest/>`_: py.test is used instead of unittest for its test runner but
also for its syntax. So you should write your tests using `pytest <http://pytest.org/latest/>`_
instead of unittest and you should not use the built-in ``TestCase``.

You can run the whole test suite using the following command:

.. code-block:: bash

  $ make tests

Code coverage should not decrease with pull requests! You can easily get the code coverage of the
project using the following command:

.. code-block:: bash

  $ make coverage

Using the issue tracker
-----------------------

You should use the `project's issue tracker <https://github.com/ellmetha/neojsonrpc/issues>`_ if
you've found a bug or if you want to propose a new feature. Don't forget to include as many details
as possible in your tickets (eg. tracebacks if this is appropriate).
