###############
Getting started
###############

Requirements
============

* `Python`_ 3.4+
* `Requests`_ 2.0+

Installation
============

To install NeoJsonRPC, please use pip_ (or pipenv_) as follows:

.. code-block:: shell

    $ pip install neojsonrpc

Basic usage
===========

In order to interact with the NEO JSON-RPC interface, all you have to do is to initialize a
``neojsonrpc.Client`` instance and to call one of the
`JSON-RPC methods <http://docs.neo.org/en-us/node/api.html>`_ provided by the NEO nodes. For example
you can get the block count of the NEO TestNet using:

.. code-block:: python

    >>> from neojsonrpc import Client
    >>> testnet_client = Client.for_testnet()
    >>> client.get_block_count()
    973369


.. _pip: https://github.com/pypa/pip
.. _pipenv: https://github.com/pypa/pipenv
.. _Python: https://www.python.org
.. _Requests: http://docs.python-requests.org/en/master/
