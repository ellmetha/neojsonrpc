"""
    NEO JSON-RPC client exceptions
    ==============================

    This module defines top-level exceptions that can be used by the NEO JSON-RPC client
    implementation.

"""


class JSONRPCError(Exception):
    """ Base exception for all exceptions that can be raised by the NEO JSON-RPC client. """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg or super(JSONRPCError, self).__str__()


class TransportError(JSONRPCError):
    """ Raised when an error occurs related to the connection with the JSON-RPC server. """

    def __init__(self, msg, response):
        super(ProtocolError, self).__init__(msg)
        self.response = response


class ProtocolError(JSONRPCError):
    """ Raised when an error occurs related to the JSON-RPC protocol / the NEO JSON-RPC methods. """

    def __init__(self, msg, response, data=None):
        super(ProtocolError, self).__init__(msg)
        self.response = response
        self.data = data
