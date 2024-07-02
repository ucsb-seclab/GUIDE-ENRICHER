from Mainnet import EthMainnet


class OtherContract:

    def __init__(self, chain):
        self.name = 'OTHER'
        self.chain = chain
        self.chain.set_balance_of_addr('OTHER', 10)

    def transfer(self, args):
        called_addr = args.get('called_addr')
        self.chain.commit({
            'txn': EthMainnet.get_transaction_hash(called_addr),
            'from': called_addr,
            'to': 'OTHER',
            'method': 'transfer',
            'transaction': 2,
            'block': self.chain.get_current_block_id_update(),
            'gas': self.chain.get_gas_price(),
            'args': None
        })
