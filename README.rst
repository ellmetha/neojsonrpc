neojsonrpc
##########

.. image:: https://img.shields.io/travis/ellmetha/neojsonrpc.svg
    :target: https://travis-ci.org/ellmetha/neojsonrpc
    :alt: Build status

.. image:: https://img.shields.io/codecov/c/github/ellmetha/neojsonrpc.svg
    :target: https://codecov.io/github/ellmetha/neojsonrpc
    :alt: Codecov status

|

**Neojsonrpc** is a Python JSON-RPC client for the NEO blockchain. It implements the JSON-RPC
methods of the API interface provided by NEO nodes (minus the methods requiring an opened wallet).
The client also provides a high-level interface to invoke contract methods on the NEO blockchain.

.. contents:: Table of Contents
    :local:

Requirements
============

Python_ 3.4+, Requests_ 2.0+.

Installation
============

To install neojsonrpc, please use pip_ (or pipenv_) as follows:

.. code-block:: shell

    $ pip install neojsonrpc

Basic usage
===========

The first step to interact with the NEO JSON-RPC interface is to initialize a `neojsonrpc.Client`
instance. The following examples respectively show how to get clients for the TestNet, the MainNet
and an hypothetical local PrivNet:

.. code-block:: python

    >>> from neojsonrpc import Client
    >>> testnet_client = Client.for_testnet()
    >>> mainnet_client = Client.for_mainnet()
    >>> privnet_client = Client(host='localhost', port='30333')

Then you can easily call some of the `JSON-RPC methods <http://docs.neo.org/en-us/node/api.html>`_
provided by NEO nodes. Here are some examples:

.. code-block:: python

    >>> from neojsonrpc import Client
    >>> client = Client.for_testnet()
    >>> client.get_block_count()
    973369
    >>> client.get_contract_state('2c0fdfa9592814b0a938219e218e3a6b08615acd')
    {'author': 'foobar',
     'code_version': '0.3',
    # [...]
    }

You can also invoke smart contract functions using the following methods:

.. code-block:: python

    >>> from neojsonrpc import Client
    >>> client = Client.for_testnet()
    >>> result = client.invoke_function('34af1b6634fcd7cfcff0158965b18601d3837e32', 'symbol', [])
    {'gas_consumed': '0.217',
     'stack': [{'type': 'ByteArray', 'value': bytearray(b'TKN')}],
     'state': 'HALT, BREAK'}
    >>> # Another convenient way to do the same operation is as follows:
    >>> client.contract('34af1b6634fcd7cfcff0158965b18601d3837e32').symbol()
    {'gas_consumed': '0.217',
     'stack': [{'type': 'ByteArray', 'value': bytearray(b'TKN')}],
     'state': 'HALT, BREAK'}

Authors
=======

Morgan Aubert (`@ellmetha <https://github.com/ellmetha>`_) and contributors_. See ``AUTHORS`` for
more details.

.. _contributors: https://github.com/ellmetha/neojsonrpc/contributors

License
=======

MIT. See ``LICENSE`` for more details.


.. _pip: https://github.com/pypa/pip
.. _pipenv: https://github.com/pypa/pipenv
.. _Python: https://www.python.org/
.. _Requests: http://docs.python-requests.org/en/master/
