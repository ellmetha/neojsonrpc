import unittest.mock

import pytest
from requests.exceptions import HTTPError

from neojsonrpc import Client
from neojsonrpc.exceptions import ProtocolError, TransportError


class TestClient:
    @unittest.mock.patch('requests.Session.post')
    def test_raises_a_transport_error_if_an_unsuccessful_is_sent_back_from_the_rpc_server(
            self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=500, content='ERROR')
        mocked_response.raise_for_status.side_effect = HTTPError(response=mocked_response)
        mocked_post.return_value = mocked_response
        client = Client.for_testnet()
        with pytest.raises(TransportError):
            client.get_block_count()

    @unittest.mock.patch('requests.Session.post')
    def test_raises_a_protocol_error_if_a_response_cannot_be_deserialized(self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='BAD')
        mocked_response.json.side_effect = ValueError()
        mocked_post.return_value = mocked_response
        client = Client.for_testnet()
        with pytest.raises(ProtocolError):
            client.get_block_count()

    @unittest.mock.patch('requests.Session.post')
    def test_raises_a_protocol_error_if_an_error_is_present_in_the_response(
            self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {'error': {'message': 'ERROR'}}
        mocked_post.return_value = mocked_response
        client = Client.for_testnet()
        with pytest.raises(ProtocolError):
            client.get_block_count()

    @unittest.mock.patch('requests.Session.post')
    def test_raises_a_protocol_error_if_result_data_is_not_present_in_the_response(
            self, mocked_post):
        mocked_response = unittest.mock.Mock(status_code=200, content='{}')
        mocked_response.json.return_value = {}
        mocked_post.return_value = mocked_response
        client = Client.for_testnet()
        with pytest.raises(ProtocolError):
            client.get_block_count()
