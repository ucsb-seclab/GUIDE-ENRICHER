import random

import gym
import numpy as np
from ray.rllib.env import EnvContext

from Contract import TornadoCashContract, OtherContract
from Mainnet import EthMainnet
from Utils import Mutation, UserProvisioning, LoadEvader, Util
from Wallet import Wallet

@DeprecationWarning
class TornadoCashGameEnvForDetector(gym.Env):

    def __init__(self, env_config: EnvContext):

        self.bloc_size = env_config.get('block_size')
        self.evader_address_range_starts = env_config.get('evader_address_range_starts')
        self.evader_address_range_end = env_config.get('evader_address_range_end')
        self.evader_mutable_address_range_start = env_config.get('evader_mutable_address_range_start')
        self.evader_mutable_address_range_end = env_config.get('evader_mutable_address_range_end')
        self.crowd_address_range_starts = env_config.get('crowd_address_range_starts')
        self.no_of_crowd = env_config.get('no_of_crowd')
        self.no_of_wallets_for_each_crowd = env_config.get('no_of_wallets_for_each_crowd_agent')
        self.amount_of_money_in_each_crowd = env_config.get('amount_of_money_in_each_crowd')

        self.evader_checkpoint_path = env_config.get('evader_checkpoint_path')
        self.evader_config = env_config.get('evader_config')
        # self.evader_wallets_1 = env_config.get('evader_wallets')

        self.total_notes = []

        self.chain = EthMainnet(self.bloc_size)
        self.tc = TornadoCashContract(self.chain)
        self.other = OtherContract(self.chain)
        self.agent = LoadEvader(checkpoint_path=self.evader_checkpoint_path, config=self.evader_config)
        self.wallets = {
            0: Wallet(chain=self.chain, wid=0, initial_money=3),
            1: Wallet(chain=self.chain, wid=1, initial_money=2),
            2: Wallet(chain=self.chain, wid=2, initial_money=0),
            3: Wallet(chain=self.chain, wid=3, initial_money=0),
            4: Wallet(chain=self.chain, wid=4, initial_money=0),
        }
        Mutation.generate_mutual_transactions(chain=self.chain, wallet_list=self.wallets,
                                              mutable_address_range=(self.evader_mutable_address_range_start,
                                                                     self.evader_mutable_address_range_end))
        self.crowd = [
            UserProvisioning(chain=self.chain, address_range_starts=self.crowd_address_range_starts + (
                    self.no_of_wallets_for_each_crowd * i),
                             address_range_end=self.crowd_address_range_starts + (
                                     self.no_of_wallets_for_each_crowd * i) + self.no_of_wallets_for_each_crowd,
                             _money_in_list=[self.amount_of_money_in_each_crowd] * self.no_of_wallets_for_each_crowd)
            for i in range(self.no_of_crowd)]

        self.observation_space = gym.spaces.Box(low=-10, high=10000, shape=(5, 6), dtype=np.float64)
        self.action_space = gym.spaces.Box(low=0, high=1, shape=(5,), dtype=int)

        self.state_evader = np.array([
            1,  # action
            0,  # wait time
            0,  # deposit call address
            0,  # withdraw call address
            len(self.total_notes),  # number of deposits
            self.chain.get_balance_of_addr(0),  # balance deposit call address
            self.chain.get_balance_of_addr(0),  # balance withdraw call address
            self.chain.get_balance_of_addr('TC')  # balance TC contract
        ])
        self.start = 0
        self.end = 0
        self.state = Util.slice(self.chain.get_main_net_txn(), self.start, self.end)

        self.no_steps = 0

    def reset(self):
        self.chain = EthMainnet(self.bloc_size)
        self.tc = TornadoCashContract(self.chain)
        self.other = OtherContract(self.chain)
        self.agent = LoadEvader(checkpoint_path=self.evader_checkpoint_path, config=self.evader_config)
        self.wallets = {
            0: Wallet(chain=self.chain, wid=0, initial_money=3),
            1: Wallet(chain=self.chain, wid=1, initial_money=2),
            2: Wallet(chain=self.chain, wid=2, initial_money=0),
            3: Wallet(chain=self.chain, wid=3, initial_money=0),
            4: Wallet(chain=self.chain, wid=4, initial_money=0),
        }
        Mutation.generate_mutual_transactions(chain=self.chain, wallet_list=self.wallets,
                                              mutable_address_range=(self.evader_mutable_address_range_start,
                                                                     self.evader_mutable_address_range_end))
        self.crowd = [
            UserProvisioning(chain=self.chain, address_range_starts=self.crowd_address_range_starts + (
                    self.no_of_wallets_for_each_crowd * i),
                             address_range_end=self.crowd_address_range_starts + (
                                     self.no_of_wallets_for_each_crowd * i) + self.no_of_wallets_for_each_crowd,
                             _money_in_list=[self.amount_of_money_in_each_crowd] * self.no_of_wallets_for_each_crowd)
            for i in range(self.no_of_crowd)]

        self.state_evader = np.array([
            1,  # action
            0,  # wait time
            0,  # deposit call address
            0,  # withdraw call address
            len(self.total_notes),  # number of deposits
            self.chain.get_balance_of_addr(0),  # balance deposit call address
            self.chain.get_balance_of_addr(0),  # balance withdraw call address
            self.chain.get_balance_of_addr('TC')  # balance TC contract
        ])

        self.start = 0
        self.end = 0
        self.state = Util.slice(self.chain.get_main_net_txn(), self.start, self.end)

        self.no_steps = 0

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
                    wallet.send_transaction(contract=self.tc, function='deposit', args=note)
                    user.set_note(note)

                elif _ACTION == 0 and user.get_notes():
                    note = random.choices(user.get_notes(), k=1)[0]
                    wallet = wallets[_out_addr_wallet_id]
                    wallet.send_transaction(contract=self.tc, function='withdraw', args=note)
                    user.remove_note(note)
            else:
                addr_wallet_id = random.choices(wallets_addresses, k=1)[0]
                wallet = wallets[addr_wallet_id]
                wallet.send_transaction(contract=self.other, function=None, args=None)

    def _step_feed(self):
        # EVADER
        evader = self.agent.get_trainer().compute_action(self.state_evader)
        ACTION = evader.get('action')
        AGENT_WAITING_TIME = evader.get('time')
        DEPOSIT_CALL_ADDR = evader.get('deposit_call_address')
        WITHDRAW_CALL_ADDR_OR_IN_ADDR = evader.get('withdraw_call_address')

        if ACTION == 1:
            note = {'from': DEPOSIT_CALL_ADDR, 'to': WITHDRAW_CALL_ADDR_OR_IN_ADDR}
            wallet = self.wallets[DEPOSIT_CALL_ADDR]
            wallet.send_transaction(contract=self.tc, function='deposit', args=note)
            self.total_notes.append(note)
        if ACTION == 0 and self.total_notes:
            note = random.choices(self.total_notes, k=1)[0]
            wallet = self.wallets[WITHDRAW_CALL_ADDR_OR_IN_ADDR]
            wallet.send_transaction(contract=self.tc, function='withdraw', args=note)
            self.total_notes.remove(note)

        # CROUD
        self._crowd_steps(num_of_crowd_steps=AGENT_WAITING_TIME)

        self.state_evader = np.array([
            ACTION,  # action
            AGENT_WAITING_TIME,  # wait time
            DEPOSIT_CALL_ADDR,  # deposit call address
            WITHDRAW_CALL_ADDR_OR_IN_ADDR,  # withdraw call address
            len(self.total_notes),  # number of deposits
            self.chain.get_balance_of_addr(DEPOSIT_CALL_ADDR),  # balance deposit call address
            self.chain.get_balance_of_addr(WITHDRAW_CALL_ADDR_OR_IN_ADDR),  # balance withdraw call address
            self.chain.get_balance_of_addr('TC')  # balance TC contract
        ])

    def step(self, action):

        self._step_feed()
        print(f'step no:\t{self.no_steps}')
        # DETECTOR
        RESULT_TABLE = list(zip(self.state, action))
        reward = 0
        for _data, _action in RESULT_TABLE:
            if (Util.check(address=_data[0],
                           evader_address_range=(
                                   self.evader_address_range_starts, self.evader_address_range_end)) or Util.check(
                address=_data[1],
                evader_address_range=(
                        self.evader_address_range_starts, self.evader_address_range_end))) and _action == 1:
                reward = 1
            elif (Util.check(address=_data[0],
                             evader_address_range=(
                                     self.evader_address_range_starts, self.evader_address_range_end)) or Util.check(
                address=_data[1],
                evader_address_range=(
                        self.evader_address_range_starts, self.evader_address_range_end))) and _action == 0:
                reward = -1
            else:
                reward = 0

        self.start = self.end
        self.end += 5
        self.state = Util.slice(self.chain.get_main_net_txn(), self.start, self.end)

        done = False
        if self.no_steps == 50:
            done = True
            print(f'done is set to {done}')
        self.no_steps += 1
        info = {}

        return self.state, reward, done, info
