"""
    NEO JSON-RPC client
    ===================

    This module defines the ``Client`` class allowing to interact with the JSON-RPC endpoints.

"""

import binascii
import json

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError

from .constants import JSONRPCMethods
from .exceptions import ProtocolError, TransportError
from .utils import decode_contract_result, encode_params


class Client:
    """ The NEO JSON-RPC client class. """

    def __init__(self, host=None, port=None, tls=False, http_max_retries=None):
        # Initializes attributes related to the client settings (host, port, etc).
        self.host = host or 'localhost'
        self.port = port or 30333
        self.tls = tls
        self.session = requests.Session()
        self.session.mount(self.host, HTTPAdapter(max_retries=http_max_retries or 3))

        # Initializes an "ID counter" that'll be used to forge each request to the JSON-RPC
        # endpoint. The "id" parameter is "required" in order to help clients sort responses out.
        # In the case of the current client, we'll just ensure that this value gets incremented
        # after each request made to the JSON-RPC endpoint.
        self._id_counter = 0

    @classmethod
    def for_mainnet(cls):
        """ Creates a ``Client`` instance for use with the NEO Main Net. """
        return cls(host='seed3.neo.org', port=10331, tls=True)

    @classmethod
    def for_testnet(cls):
        """ Creates a ``Client`` instance for use with the NEO Test Net. """
        return cls(host='seed3.neo.org', port=20331, tls=True)

    ####################
    # JSON-RPC METHODS #
    ####################

    def get_account_state(self, address, **kwargs):
        """ Returns the account state information associated with a specific address.

        :param address: a 34-bit length address (eg. AJBENSwajTzQtwyJFkiJSv7MAaaMc7DsRz)
        :type address: str
        :return: dictionary containing the account state information
        :rtype: dict

        """
        return self._call(JSONRPCMethods.GET_ACCOUNT_STATE.value, params=[address, ], **kwargs)

    def get_asset_state(self, asset_id, **kwargs):
        """ Returns the asset information associated with a specific asset ID.

        :param asset_id:
            an asset identifier (the transaction ID of the RegistTransaction when the asset is
            registered)
        :type asset_id: str
        :return: dictionary containing the asset state information
        :rtype: dict

        """
        return self._call(JSONRPCMethods.GET_ASSET_STATE.value, params=[asset_id, ], **kwargs)

    def get_best_block_hash(self, **kwargs):
        """ Returns the hash of the tallest block in the main chain.

        :return: hash of the tallest block in the chain
        :rtype: str

        """
        return self._call(JSONRPCMethods.GET_BEST_BLOCK_HASH.value, **kwargs)

    def get_block(self, block_hash, verbose=True, **kwargs):
        """ Returns the block information associated with a specific hash value or block index.

        :param block_hash: a block hash value or a block index (block height)
        :param verbose:
            a boolean indicating whether the detailed block information should be returned in JSON
            format (otherwise the block information is returned as an hexadecimal string by the
            JSON-RPC endpoint)
        :type block_hash: str or int
        :type verbose: bool
        :return:
            dictionary containing the block information (or an hexadecimal string if verbose is set
            to False)
        :rtype: dict or str

        """
        return self._call(
            JSONRPCMethods.GET_BLOCK.value, params=[block_hash, int(verbose), ], **kwargs)

    def get_block_count(self, **kwargs):
        """ Returns the number of blocks in the chain.

        :return: number of blocks in the chain
        :rtype: int

        """
        return self._call(JSONRPCMethods.GET_BLOCK_COUNT.value, **kwargs)

    def get_block_hash(self, block_index, **kwargs):
        """ Returns the hash value associated with a specific block index.

        :param block_index: a block index (block height)
        :type block_index: int
        :return: hash of the block associated with the considered index
        :rtype: str

        """
        return self._call(JSONRPCMethods.GET_BLOCK_HASH.value, [block_index, ], **kwargs)

    def get_block_sys_fee(self, block_index, **kwargs):
        """ Returns the system fees associated with a specific block index.

        :param block_index: a block index (block height)
        :type block_index: int
        :return: system fees of the block, expressed in NeoGas units
        :rtype: str

        """
        return self._call(JSONRPCMethods.GET_BLOCK_SYS_FEE.value, [block_index, ], **kwargs)

    def get_connection_count(self, **kwargs):
        """ Returns the current number of connections for the considered node.

        :return: number of connections for the node
        :rtype: int

        """
        return self._call(JSONRPCMethods.GET_CONNECTION_COUNT.value, **kwargs)

    def get_contract_state(self, script_hash, **kwargs):
        """ Returns the contract information associated with a specific script hash.

        :param script_hash: contract script hash
        :type script_hash: str
        :return: dictionary containing the contract information
        :rtype: dict

        """
        return self._call(JSONRPCMethods.GET_CONTRACT_STATE.value, [script_hash, ], **kwargs)

    def get_raw_mem_pool(self, **kwargs):
        """ Returns a list of unconfirmed transactions in memory associated with the node.

        :return: list of unconfirmed transaction hashes
        :rtype: list

        """
        return self._call(JSONRPCMethods.GET_RAW_MEM_POOL.value, **kwargs)

    def get_raw_transaction(self, tx_hash, verbose=True, **kwargs):
        """ Returns detailed information associated with a specific transaction hash.

        :param tx_hash: transaction hash
        :param verbose:
            a boolean indicating whether the detailed transaction information should be returned in
            JSON format (otherwise the transaction information is returned as an hexadecimal string
            by the JSON-RPC endpoint)
        :type tx_hash: str
        :type verbose: bool
        :return:
            dictionary containing the transaction information (or an hexadecimal string if verbose
            is set to False)
        :rtype: dict or str

        """
        return self._call(
            JSONRPCMethods.GET_RAW_TRANSACTION.value, params=[tx_hash, int(verbose), ], **kwargs)

    def get_storage(self, script_hash, key, **kwargs):
        """ Returns the value stored in the storage of a contract script hash for a given key.

        :param script_hash: contract script hash
        :param key: key to look up in the storage
        :type script_hash: str
        :type key: str
        :return: value associated with the storage key
        :rtype: bytearray

        """
        hexkey = binascii.hexlify(key.encode('utf-8')).decode('utf-8')
        hexresult = self._call(
            JSONRPCMethods.GET_STORAGE.value, params=[script_hash, hexkey, ], **kwargs)
        try:
            assert hexresult
            result = bytearray(binascii.unhexlify(hexresult.encode('utf-8')))
        except AssertionError:
            result = hexresult
        return result

    def get_tx_out(self, tx_hash, index, **kwargs):
        """ Returns the transaction output information corresponding to a hash and index.

        :param tx_hash: transaction hash
        :param index:
            index of the transaction output to be obtained in the transaction (starts from 0)
        :type tx_hash: str
        :type index: int
        :return: dictionary containing the transaction output
        :rtype: dict

        """
        return self._call(JSONRPCMethods.GET_TX_OUT.value, params=[tx_hash, index, ], **kwargs)

    def get_peers(self, **kwargs):
        """ Returns a list of nodes that the node is currently connected/disconnected from.

        :return: dictionary containing the nodes the current node is connected/disconnected from
        :rtype: dict

        """
        return self._call(JSONRPCMethods.GET_PEERS.value, **kwargs)

    def get_version(self, **kwargs):
        """ Returns version information about the current node.

        :return: dictionary containing version information about the current node
        :rtype: dict

        """
        return self._call(JSONRPCMethods.GET_VERSION.value, **kwargs)

    def invoke(self, script_hash, params, **kwargs):
        """ Invoke a contract with given parameters and returns the result.

        It should be noted that the name of the function invoked in the contract should be part of
        paramaters.

        :param script_hash: contract script hash
        :param params: list of paramaters to be passed in to the smart contract
        :type script_hash: str
        :type params: list
        :return: result of the invocation
        :rtype: bytearray

        """
        contract_params = encode_params(params)
        raw_result = self._call(
            JSONRPCMethods.INVOKE.value, [script_hash, contract_params, ], **kwargs)
        return decode_contract_result(raw_result)

    ##################################
    # PRIVATE METHODS AND PROPERTIES #
    ##################################

    def _call(self, method, params=None, request_id=None):
        """ Calls the JSON-RPC endpoint. """
        params = params or []

        # Determines which 'id' value to use and increment the counter associated with the current
        # client instance if applicable.
        rid = request_id or self._id_counter
        if request_id is None:
            self._id_counter += 1

        # Prepares the payload and the headers that will be used to forge the request.
        payload = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': rid}
        headers = {'Content-Type': 'application/json'}
        scheme = 'https' if self.tls else 'http'
        url = '{}://{}:{}'.format(scheme, self.host, self.port)

        # Calls the JSON-RPC endpoint!
        try:
            response = self.session.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
        except HTTPError:
            raise TransportError(
                'Go unsuccessful response from server (status code: {})'.format(
                    response.status_code),
                response=response)

        # Ensures the response body can be deserialized to JSON.
        try:
            response_data = response.json()
        except ValueError as e:
            raise ProtocolError(
                'Unable to deserialize response body: {}'.format(e), response=response)

        # Properly handles potential errors.
        if response_data.get('error'):
            code = response_data['error'].get('code', '')
            message = response_data['error'].get('message', '')
            raise ProtocolError(
                'Error[{}] {}'.format(code, message), response=response, data=response_data)
        elif 'result' not in response_data:
            raise ProtocolError(
                'Response is empty (result field is missing)', response=response,
                data=response_data)

        return response_data['result']
