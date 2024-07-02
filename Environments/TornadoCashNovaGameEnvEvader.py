import copy
import random
import time
import warnings
from collections import defaultdict

import gym  # Ray version: 2.0.0
# import gymnasium as gym # for env Ray version: 2.4.0
import numpy as np
from ray.rllib.env import EnvContext

from Contract import TornadoCashNovaContract, OtherContract
from Heuristics import Tutela
from Mainnet import EthMainnet
from Utils import NovaUserProvisioning, Mutation

warnings.filterwarnings("ignore")


class TornadoCashNovaGameEnvEvader(gym.Env):

    def __init__(self, env_config: EnvContext):

        self.bloc_size = env_config.get('block_size')
        self.max_wait_time = env_config.get('max_wait_time')
        self.no_addresses_agent_challenge_table = env_config.get('no_addresses_agent_challenge_table')
        self.ctable = env_config.get('agent_challenge_table')
        self.agent_address_range_starts = env_config.get('agent_address_range_starts')
        self.agent_address_range_end = env_config.get('agent_address_range_end')
        self.agent_mutable_address_range_start = env_config.get('agent_mutable_address_range_start')
        self.agent_mutable_address_range_end = env_config.get('agent_mutable_address_range_end')
        self.crowd_address_range_starts = env_config.get('crowd_address_range_starts')
        self.no_of_crowd = env_config.get('no_of_crowd')
        self.no_of_wallets_for_each_crowd = env_config.get('no_of_wallets_for_each_crowd_agent')
        self.amount_of_money_in_each_crowd = env_config.get('amount_of_money_in_each_crowd')

        self.chain = EthMainnet(self.bloc_size)
        self.tc = TornadoCashNovaContract(self.chain)  # TornadoCash contract (will be Nova)
        self.other = OtherContract(self.chain)
        self.detector = Tutela(chain=self.chain, contract=self.tc)  # Add other Heuristics
        self.agent_challenge_table = copy.deepcopy(self.ctable)
        self.agent_challenge_table_addresses = list(range(len(self.agent_challenge_table)))
        self.agent = NovaUserProvisioning(chain=self.chain, address_range_starts=self.agent_address_range_starts,
                                          address_range_end=self.agent_address_range_end,
                                          _money_in_list=self.ctable)
        self.agent_wallets = self.agent.get_wallets()
        Mutation.generate_mutual_transactions(chain=self.chain, wallet_list=self.agent_wallets,
                                              mutable_address_range=(self.agent_mutable_address_range_start,
                                                                     self.agent_mutable_address_range_end))
        self.crowd = [
            NovaUserProvisioning(chain=self.chain, address_range_starts=self.crowd_address_range_starts + (
                    self.no_of_wallets_for_each_crowd * i),
                                 address_range_end=self.crowd_address_range_starts + (
                                         self.no_of_wallets_for_each_crowd * i) + self.no_of_wallets_for_each_crowd,
                                 _money_in_list=[
                                                    self.amount_of_money_in_each_crowd] * self.no_of_wallets_for_each_crowd)
            for i in range(self.no_of_crowd)]

        self.is_torn_mining_enable = False

        self.observation_space = gym.spaces.Box(low=-2, high=10000000, shape=(17,), dtype=np.float64)
        self.action_space = gym.spaces.Dict({'action': gym.spaces.Discrete(2),
                                             'time': gym.spaces.Discrete(self.max_wait_time),
                                             'deposit_call_address': gym.spaces.Discrete(
                                                 self.no_addresses_agent_challenge_table),
                                             'withdraw_call_address': gym.spaces.Discrete(
                                                 self.agent_address_range_end),
                                             'deposit_amount': gym.spaces.Discrete(3),
                                             'withdraw_amount': gym.spaces.Discrete(3),
                                             })

        self.state = np.array([
            1,  # action
            0,  # wait time
            0,  # deposit call address
            len(self.agent_challenge_table),  # withdraw call address
            self.agent.get_total_no_of_notes(),  # number of deposits
            self.chain.get_balance_of_addr(0),  # balance of deposit call address
            self.chain.get_balance_of_addr(len(self.agent_challenge_table)),  # balance of withdraw call address
            self.chain.get_balance_of_addr('Nova'),  # balance current TC contract
            sum(self.agent_challenge_table),  # remaining of the challenge table
            1,  # is DEPOSIT_CALL_ADDR is an address from challenge table
            1,  # is WITHDRAW_CALL_ADDR_OR_IN_ADDR is NOT an address from challenge table
            1,  # DEPOSIT_AMOUNT
            1,  # WITHDRAW_AMOUNT index
            1,  # WITHDRAW_AMOUNT
            0,  # balance of the note
            1,  # is DEPOSIT Wallet addresses has enough money to withdraw
            0  # is WITHDRAW Note  has enough money to withdraw
        ])

        self.count = 1
        self.uuid = time.time()

    def reset(self):
        self.chain = EthMainnet(self.bloc_size)
        self.tc = TornadoCashNovaContract(self.chain)
        self.other = OtherContract(self.chain)
        self.detector = Tutela(chain=self.chain, contract=self.tc)
        self.agent_challenge_table = copy.deepcopy(self.ctable)
        self.agent_challenge_table_addresses = list(range(len(self.agent_challenge_table)))
        self.agent = NovaUserProvisioning(chain=self.chain, address_range_starts=self.agent_address_range_starts,
                                          address_range_end=self.agent_address_range_end,
                                          _money_in_list=self.ctable)
        self.agent_wallets = self.agent.get_wallets()
        Mutation.generate_mutual_transactions(chain=self.chain, wallet_list=self.agent_wallets,
                                              mutable_address_range=(self.agent_mutable_address_range_start,
                                                                     self.agent_mutable_address_range_end))
        self.crowd = [
            NovaUserProvisioning(chain=self.chain, address_range_starts=self.crowd_address_range_starts + (
                    self.no_of_wallets_for_each_crowd * i),
                                 address_range_end=self.crowd_address_range_starts + (
                                         self.no_of_wallets_for_each_crowd * i) + self.no_of_wallets_for_each_crowd,
                                 _money_in_list=[
                                                    self.amount_of_money_in_each_crowd] * self.no_of_wallets_for_each_crowd)
            for i in range(self.no_of_crowd)]

        self.is_torn_mining_enable = False

        self.state = np.array([
            1,  # action
            0,  # wait time
            0,  # deposit call address
            len(self.agent_challenge_table),
            self.agent.get_total_no_of_notes(),  # number of deposits
            self.chain.get_balance_of_addr(0),  # balance deposit call address
            self.chain.get_balance_of_addr(len(self.agent_challenge_table)),  # balance withdraw call address
            self.chain.get_balance_of_addr('Nova'),  # balance TC contract
            sum(self.agent_challenge_table),  # remaining of the challenge table
            1,  # is DEPOSIT_CALL_ADDR is an address from challenge table
            1,  # is WITHDRAW_CALL_ADDR_OR_IN_ADDR is NOT an address from challenge table
            1,  # DEPOSIT_AMOUNT
            1,  # WITHDRAW_AMOUNT index
            1,  # WITHDRAW_AMOUNT
            0,  # balance of the note
            1,  # is DEPOSIT Wallet addresses has enough money to withdraw
            0  # is WITHDRAW Note  has enough money to withdraw
        ])

        self.count = 1
        self.uuid = time.time()

        return self.state

    @staticmethod
    def address_check(in_address, picked_address):
        return picked_address in in_address

    def _crowd_steps(self, num_of_crowd_steps=2):
        for _i in range(num_of_crowd_steps):

            OTHER_OR_TC = random.randint(0, 1)
            _ACTION = random.randint(0, 1)
            _USER_ID = random.randint(0, len(self.crowd) - 1)

            user = self.crowd[_USER_ID]
            wallets = user.get_wallets()
            wallets_addresses = user.get_wallets_addresses()

            if OTHER_OR_TC == 1:
                _in_addr_wallet_id = random.choices(wallets_addresses, k=1)[0]
                _out_addr_wallet_id = random.choices(wallets_addresses, k=1)[0]

                if _ACTION == 1 and wallets[_in_addr_wallet_id].get_balance() > 0:
                    to_addr = _out_addr_wallet_id
                    note = {'from': _in_addr_wallet_id, 'to': to_addr}
                    wallet = wallets[_in_addr_wallet_id]
                    balance = wallets[_in_addr_wallet_id].get_balance()
                    deposit_amount = round(random.uniform(1, balance), 2)

                    if balance >= deposit_amount:
                        wallet.send_transaction(contract=self.tc, function='deposit', args=note, fund=deposit_amount)
                        user.set_note(note)


                elif _ACTION == 0 and user.get_notes():
                    note = random.choices(user.get_notes(), k=1)[0]
                    wallet = wallets[_out_addr_wallet_id]
                    withdraw_amount = [0.1, 0.3, 0.5, 1][random.randint(0, 3)]
                    balance = note['fund']
                    if balance >= withdraw_amount:
                        wallet.send_transaction(contract=self.tc, function='withdraw', args=note, fund=withdraw_amount)
                        user.remove_note(note)
            else:
                addr_wallet_id = random.choices(wallets_addresses, k=1)[0]
                wallet = wallets[addr_wallet_id]
                wallet.send_transaction(contract=self.other, function=None, args=None)

    def step(self, action):

        ACTION = action.get('action')
        AGENT_WAITING_TIME = action.get('time')
        DEPOSIT_CALL_ADDR = action.get('deposit_call_address')
        WITHDRAW_CALL_ADDR_OR_IN_ADDR = action.get('withdraw_call_address')
        DEPOSIT_AMOUNT = action.get('deposit_amount') + 1
        WITHDRAW_AMOUNT_INDEX = action.get('withdraw_amount')
        WITHDRAW_AMOUNT = [0.1, 0.3, 0.5, 1][WITHDRAW_AMOUNT_INDEX]
        # print(DEPOSIT_AMOUNT, WITHDRAW_AMOUNT, WITHDRAW_AMOUNT_INDEX)
        note_balance = -1
        _wallet_enough_balance = 0
        _note_enough_balance = 0

        reward = 0
        CHECK = True
        if ACTION == 1:
            if self.agent_wallets[DEPOSIT_CALL_ADDR].get_balance() > 0 and \
                    self.agent_challenge_table[DEPOSIT_CALL_ADDR] > 0 and \
                    not TornadoCashNovaGameEnvEvader.address_check(in_address=self.agent_challenge_table_addresses,
                                                                   picked_address=WITHDRAW_CALL_ADDR_OR_IN_ADDR) and \
                    TornadoCashNovaGameEnvEvader.address_check(in_address=self.agent_challenge_table_addresses,
                                                               picked_address=DEPOSIT_CALL_ADDR):
                TO_ADDR = WITHDRAW_CALL_ADDR_OR_IN_ADDR
                note = {'from': DEPOSIT_CALL_ADDR, 'to': TO_ADDR}
                wallet = self.agent_wallets[DEPOSIT_CALL_ADDR]
                _balance = wallet.get_balance()
                if wallet.get_balance() >= DEPOSIT_AMOUNT:
                    _wallet_enough_balance = 1
                    wallet.send_transaction(contract=self.tc, function='deposit', args=note, fund=DEPOSIT_AMOUNT)
                    self.agent.set_note(note)
                    self.agent_challenge_table[DEPOSIT_CALL_ADDR] = max(0, self.agent_challenge_table[
                        DEPOSIT_CALL_ADDR] - DEPOSIT_AMOUNT)
                    reward = (-1 if self.detector.run_nova_heuristics_check() else 1)
                    # reward = 1
                else:
                    reward = -1
                # print(f'DEPOSIT => UUID {self.uuid} count {self.count}', _balance, wallet.get_balance(),
                #       DEPOSIT_AMOUNT,
                #       _balance >= DEPOSIT_AMOUNT,
                #       self.agent_challenge_table, self.agent.get_notes(), self.chain.get_balance_of_addr('Nova'))
            else:
                CHECK = False
                reward = -2

        elif ACTION == 0:
            if self.agent.get_notes():
                note = random.choices(self.agent.get_notes(), k=1)[0]
                note_balance = note['fund']
                if note['fund'] >= WITHDRAW_AMOUNT:
                    _note_enough_balance = 1
                    wallet = self.agent_wallets[WITHDRAW_CALL_ADDR_OR_IN_ADDR]
                    wallet.send_transaction(contract=self.tc, function='withdraw', args=note, fund=WITHDRAW_AMOUNT)
                    self.agent.remove_note(note)
                    reward = (-1 if self.detector.run_nova_heuristics_check() else 1)
                    # reward = 1
                elif note['fund'] < 0.1:
                    _note_enough_balance = 1
                    wallet = self.agent_wallets[WITHDRAW_CALL_ADDR_OR_IN_ADDR]
                    wallet.send_transaction(contract=self.tc, function='withdraw', args=note, fund=note['fund'])
                    self.agent.remove_note(note)
                    reward = (-1 if self.detector.run_nova_heuristics_check() else 1)
                    # reward = 1
                else:
                    reward = -1
                # print(f'WITHDRAW => UUID {self.uuid} count {self.count}', note_balance, WITHDRAW_AMOUNT,
                #       note_balance >= WITHDRAW_AMOUNT,
                #       self.agent_challenge_table, note, self.agent.get_notes(), self.chain.get_balance_of_addr('Nova'))
            else:
                CHECK = False
                reward = -2

        # CROUD
        # add a check
        if CHECK:
            self._crowd_steps(num_of_crowd_steps=AGENT_WAITING_TIME)

        self.state = np.array([
            ACTION,  # action
            AGENT_WAITING_TIME,  # wait time
            DEPOSIT_CALL_ADDR,  # deposit call address
            WITHDRAW_CALL_ADDR_OR_IN_ADDR,  # withdraw call address
            self.agent.get_total_no_of_notes(),  # number of deposits
            self.chain.get_balance_of_addr(DEPOSIT_CALL_ADDR),  # balance deposit call address
            self.chain.get_balance_of_addr(WITHDRAW_CALL_ADDR_OR_IN_ADDR),  # balance withdraw call address
            self.chain.get_balance_of_addr('Nova'),  # balance TC contract
            sum(self.agent_challenge_table),  # remaining of the challenge table
            1 if TornadoCashNovaGameEnvEvader.address_check(in_address=self.agent_challenge_table_addresses,
                                                            picked_address=DEPOSIT_CALL_ADDR) else 0,
            # is DEPOSIT_CALL_ADDR is an address from challenge table
            1 if not TornadoCashNovaGameEnvEvader.address_check(in_address=self.agent_challenge_table_addresses,
                                                                picked_address=WITHDRAW_CALL_ADDR_OR_IN_ADDR) else 0,
            # is WITHDRAW_CALL_ADDR_OR_IN_ADDR is NOT an address from challenge table
            DEPOSIT_AMOUNT,  # DEPOSIT_AMOUNT
            WITHDRAW_AMOUNT_INDEX,  # WITHDRAW_AMOUNT index
            WITHDRAW_AMOUNT,  # WITHDRAW_AMOUNT
            note_balance,  # balance of the note
            _wallet_enough_balance,  # is DEPOSIT Wallet addresses has enough money to withdraw
            _note_enough_balance  # is WITHDRAW Note  has enough money to withdraw
        ])

        done = False
        if sum(self.agent_challenge_table) == 0 and not self.agent.get_notes():
            done = True

        # time.sleep(5)
        self.count += 1

        info = {'chain': self.chain.get_main_net_txn(),
                'challenge table': self.agent_challenge_table,
                'balance table': self.chain.get_balance_table(),
                'heuristic reward history': self.detector.get_step_heuristic_reward_history(),
                'count': self.count,
                'is done': done,
                'note balance': self.agent.get_notes()
                }

        return self.state, reward, done, info
