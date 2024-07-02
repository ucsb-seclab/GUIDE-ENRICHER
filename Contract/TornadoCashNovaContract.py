import hashlib
import random
import time

import pandas as pd

from Mainnet import EthMainnet
from collections import defaultdict


class TornadoCashNovaContract:

    def __init__(self, chain):
        self.name = 'Nova'
        self._merkle_tree = []
        self._merkle_tree_logger = pd.DataFrame(
            columns=['note hash', 'from', 'to', 'fund', 'in block'])  # log the note's fund
        self.chain = chain
        self.chain.set_balance_of_addr('Nova', 10)
        # Manage the balance of each note individually

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
        note['note hash'] = TornadoCashNovaContract.create_note_hash(note)
        return note

    # ~~ Manage the balance of each note individually ~~
    @staticmethod
    def get_balance_of_note(note):
        return note['fund']

    @staticmethod
    def set_balance_of_note(note, value):
        note['fund'] = value
        return note

    @staticmethod
    def update_balance_of_note(note, value):
        note['fund'] -= value
        return note

    def log_note(self, note):
        note['in block'] = self.chain.get_current_block_id()
        return note

    # -----------------------------

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
        # arbitrary value of the deposit
        _fund = args.get('fund')  # pass from Wallet
        note = TornadoCashNovaContract.update_note(_note)
        # arbitrary value of the deposit
        note = TornadoCashNovaContract.set_balance_of_note(note, _fund)
        self._merkle_tree.append(note)
        self.chain.commit({
            'txn': EthMainnet.get_transaction_hash(called_addr),
            'from': called_addr,
            'to': 'Nova',
            'method': 'deposit',
            'transaction': _fund,  # arbitrary value of the deposit
            'block': self.chain.get_current_block_id_update(),
            'gas': self.chain.get_gas_price(),
            'args': note
        })
        self._merkle_tree_logger = pd.concat(
            [self._merkle_tree_logger, pd.DataFrame([self.log_note(note)])]).reset_index(drop=True)

        return 0

    def withdraw(self, args):
        note = args.get('note')
        _fund = args.get('fund')
        called_addr = args.get('called_addr')
        if self.verify(note) and note['fund'] > 0:
            note['fund'] -= _fund
            if note['fund'] == 0:
                self._merkle_tree.remove(note)
            # record the function call
            self.chain.commit({
                'txn': EthMainnet.get_transaction_hash(called_addr),
                'from': called_addr,
                'to': 'Nova',
                'method': 'withdraw',
                'transaction': 0,
                'block': self.chain.get_current_block_id_update(),
                'gas': self.chain.get_gas_price(),
                'args': note
            })
            # record the internal txn
            self.chain.commit({
                'txn': EthMainnet.get_transaction_hash(note.get('to')),
                'from': 'Nova',
                'to': note.get('to'),
                'method': 'internal',
                'transaction': _fund,
                'block': self.chain.get_current_block_id_update(),
                'gas': self.chain.get_gas_price(),
                'args': None
            })
            return 0
        else:
            return 1
