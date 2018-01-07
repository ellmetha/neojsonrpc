"""
    NEO JSON-RPC client
    ===================

    The NEO JSON-RPC client implements the JSON-RPC methods provided by the API interface of NEO
    nodes (see: http://docs.neo.org/en-us/node/api.html). NEO nodes can expose a JSON-RPC interface
    to allow clients to obtain blockchain data in order to ease the development of blockchain
    applications. The NEO JSON-RPC client also implements several client-specific methods or
    shortcuts in order to provide more high-level interfaces for interacting with the blockchain.

"""


__version__ = '0.1.1.dev'


from .client import Client  # noqa: F401
