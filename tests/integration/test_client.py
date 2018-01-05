from neojsonrpc import Client


class TestClient:
    def test_can_return_the_state_of_an_account(self):
        client = Client.for_testnet()
        account = client.get_account_state('ALn85kUVLWWZdCuZfvjwbmusWH9Hx43XuF')
        assert 'balances' in account
        assert account['balances']

    def test_can_return_the_state_of_an_asset(self):
        client = Client.for_testnet()
        asset = client.get_asset_state(
            'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b')  # NEO
        assert asset['amount'] == '100000000'
        assert asset['available'] == '100000000'
        assert asset['precision'] == 0

    def test_can_return_the_best_block_hash(self):
        client = Client.for_testnet()
        best_block_hash = client.get_best_block_hash()
        assert len(best_block_hash[2:]) == 64

    def test_can_return_block_information_associated_with_a_block_hash(self):
        client = Client.for_testnet()
        block = client.get_block('9e38052ac0827e490b917bd69174cfa0fae9a7f77db18ed3cf2ee95922e0103d')
        assert block['hash'] == '0x9e38052ac0827e490b917bd69174cfa0fae9a7f77db18ed3cf2ee95922e0103d'
        assert block['index']

    def test_can_return_system_fees_associated_with_a_block_hash(self):
        client = Client.for_testnet()
        fees = client.get_block_sys_fee(966045)
        assert fees == '716234'

    def test_can_return_the_connection_count(self):
        client = Client.for_testnet()
        connection_count = client.get_connection_count()
        assert connection_count

    def test_can_return_the_state_of_a_contract(self):
        client = Client.for_testnet()
        contract = client.get_contract_state('f9572c5b119a6b5775a6af07f1cef5d310038f55')
        assert contract['hash'] == '0xf9572c5b119a6b5775a6af07f1cef5d310038f55'

    def test_can_return_a_list_of_unconfirmed_transactions_associated_with_the_node(self):
        client = Client.for_testnet()
        mempool = client.get_raw_mem_pool()
        assert isinstance(mempool, list)
