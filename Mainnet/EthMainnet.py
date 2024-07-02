import hashlib
import random
import time
from collections import defaultdict

import pandas as pd


class EthMainnet:

    def __init__(self, block_size):
        self.main_net_txn = pd.DataFrame(columns=['txn', 'from', 'to', 'method', 'transaction', 'block', 'gas', 'args'])
        self.main_net_balance = defaultdict(int)
        self.block_id = 1
        self.gas = 1
        self.BLOCK_SIZE = block_size

    @staticmethod
    def get_transaction_hash(address):
        seed = random.random()
        seed_time = time.time()
        data = "{}-{}-{}".format(address, seed, seed_time)
        hash_object = hashlib.sha1()
        hash_object.update(data.encode('utf-8'))
        hash_value = hash_object.hexdigest()
        return hash_value

    def commit(self, data):
        self.main_net_txn = pd.concat([self.main_net_txn, pd.DataFrame([data])]).reset_index(drop=True)
        self.main_net_balance[data.get('from')] -= data.get('transaction')
        self.main_net_balance[data.get('to')] += data.get('transaction')

    def get_main_net_txn(self):
        return self.main_net_txn

    def get_balance_table(self):
        return self.main_net_balance

    def get_balance_of_addr(self, addr):
        return self.main_net_balance.get(addr, 0)

    def set_balance_of_addr(self, addr, amount):
        self.main_net_balance[addr] = amount

    def get_current_block_id_update(self):
        if self.main_net_txn.shape[0] % self.BLOCK_SIZE == 0:
            self.block_id += 1
        return self.block_id

    def get_current_block_id(self):
        return self.block_id

    def get_current_block(self, block_id):
        return self.main_net_txn.loc[self.main_net_txn.block == block_id]

    def get_gas_price(self):
        if self.main_net_txn.shape[0] % self.BLOCK_SIZE == 0:
            self.gas += 1
        return self.gas
