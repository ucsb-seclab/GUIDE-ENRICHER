import hashlib
import random
import time

import pandas as pd

from Mainnet import EthMainnet


class TornadoCashContract:

    def __init__(self, chain):
        self.name = 'TC'
        self._merkle_tree = []
        self._merkle_tree_logger = pd.DataFrame(columns=['note hash', 'from', 'to', 'in block'])
        self.chain = chain
        self.chain.set_balance_of_addr('TC', 0)

    @staticmethod
    def create_note_hash(note):
        seed = random.random()
        seed_time = time.time()
        data = "{}-{}-{}-{}".format(note.get('from'), note.get('to'), seed, seed_time)
        hash_object = hashlib.sha1()
        hash_object.update(data.encode('utf-8'))
        hash_value = hash_object.hexdigest()
        return hash_value

    @staticmethod
    def update_note(note):
        note['note hash'] = TornadoCashContract.create_note_hash(note)
        return note

    def log_note(self, note):
        note['in block'] = self.chain.get_current_block_id()
        return note

    def get_origin_block_of_note(self, note_hash):
        return self._merkle_tree_logger.loc[self._merkle_tree_logger['note hash'] == note_hash]['in block'].values[0]

    def get_merkle_tree(self):
        return self._merkle_tree

    def verify(self, note):
        if note in self._merkle_tree:
            return True
        return False

    def deposit(self, args):
        called_addr = args.get('called_addr')
        _note = args.get('note')
        note = TornadoCashContract.update_note(_note)
        self._merkle_tree.append(note)
        self.chain.commit({
            'txn': EthMainnet.get_transaction_hash(called_addr),
            'from': called_addr,
            'to': 'TC',
            'method': 'deposit',
            'transaction': 1,
            'block': self.chain.get_current_block_id_update(),
            'gas': self.chain.get_gas_price(),
            'args': note
        })
        self._merkle_tree_logger = pd.concat(
            [self._merkle_tree_logger, pd.DataFrame([self.log_note(note)])]).reset_index(drop=True)

        return 0

    def withdraw(self, args):
        note = args.get('note')
        called_addr = args.get('called_addr')
        if self.verify(note):
            self._merkle_tree.remove(note)
            # record the function call
            self.chain.commit({
                'txn': EthMainnet.get_transaction_hash(called_addr),
                'from': called_addr,
                'to': 'TC',
                'method': 'withdraw',
                'transaction': 0,
                'block': self.chain.get_current_block_id_update(),
                'gas': self.chain.get_gas_price(),
                'args': note
            })
            # record the internal txn
            self.chain.commit({
                'txn': EthMainnet.get_transaction_hash(note.get('to')),
                'from': 'TC',
                'to': note.get('to'),
                'method': 'internal',
                'transaction': 1,
                'block': self.chain.get_current_block_id_update(),
                'gas': self.chain.get_gas_price(),
                'args': None
            })
            return 0
        else:
            return 1
