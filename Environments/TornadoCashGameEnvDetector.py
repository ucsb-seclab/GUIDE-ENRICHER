import gym
import numpy as np
from ray.rllib.env import EnvContext

from Contract import TornadoCashContract, OtherContract
from Environments import TornadoCashEvaderControlledEnv
from Mainnet import EthMainnet
from Utils import Util, LoadEvader


class TornadoCashGameEnvDetector(gym.Env):

    def __init__(self, env_config: EnvContext):
        self.window_size = env_config.get('window_size')
        self.bloc_size = env_config.get('block_size')
        self.evader_check_point_path = env_config.get('evader_check_point_path')
        self.evader_configs = env_config.get('evader_configs')
        self.evader_env_configs = env_config.get('evader_env_configs')
        self.evader_address_range_end = self.evader_env_configs.get('agent_address_range_end')

        self.observation_space = gym.spaces.Box(low=-10, high=10000, shape=(self.window_size, 6), dtype=np.float64)
        self.action_space = gym.spaces.Box(low=0, high=1, shape=(self.window_size,), dtype=int)

        self.chain = EthMainnet(self.bloc_size)
        self.tc = TornadoCashContract(self.chain)
        self.other = OtherContract(self.chain)

        self.evader = LoadEvader(checkpoint_path=self.evader_check_point_path, config=self.evader_configs)
        self.playground = TornadoCashEvaderControlledEnv(self.evader_env_configs, self.chain, self.tc, self.other)
        self.evader_obs = self.playground.reset()

        # set the sliding window using config
        self.start = 0
        self.end = self.window_size
        self.state = Util.slice(df=self.chain.get_main_net_txn(), start=self.start, end=self.end,
                                slice_size=self.window_size)

        self.action_history = []

    def reset(self):
        self.chain = EthMainnet(self.bloc_size)
        self.tc = TornadoCashContract(self.chain)
        self.other = OtherContract(self.chain)

        self.evader = LoadEvader(checkpoint_path=self.evader_check_point_path, config=self.evader_configs)
        self.playground = TornadoCashEvaderControlledEnv(self.evader_env_configs, self.chain, self.tc, self.other)

        # set the sliding window using config
        self.start = 0
        self.end = self.window_size
        self.state = Util.slice(df=self.chain.get_main_net_txn(), start=self.start, end=self.end,
                                slice_size=self.window_size)

        self.action_history = []

        return self.state

    @staticmethod
    def address_check(in_address, picked_address):
        return picked_address in in_address

    def step(self, action):
        reward = 0
        done = False
        if not self.evader.is_done():
            evader_action = self.evader.get_ppo_trainer().compute_action(self.evader_obs)
            self.evader_obs, evader_reward, evader_done, evader_info = self.playground.step(evader_action)
            self.evader.set_don(evader_done)
        results = list(zip(self.state, action))
        # FROM, TO, METHOD, TRANSACTIONS, BLOCK, GAS
        ADDR_RANGE = list(range(self.evader_address_range_end))
        for states, action in results:
            _from, _to, _method, _transaction, _block, _gas = states
            if _from in ADDR_RANGE and action == 1 and _to == -1 and _method == 2:
                reward += 1
            elif _from not in ADDR_RANGE and action == 1 and _to == -1 and _method == 2:
                reward -= 1
            elif _from in ADDR_RANGE and action == 0 and _to == -1 and _method == 2:
                reward -= 1
            elif _from not in ADDR_RANGE and action == 0 and _to == -1 and _method == 2:
                reward += 1
        self.state = Util.slice(df=self.chain.get_main_net_txn(), start=self.start, end=self.end,
                                slice_size=self.window_size)
        self.start = self.end
        self.end += self.window_size
        done = self.evader.is_done() and self.chain.get_main_net_txn().shape[0] == self.end
        info = {'chain': self.chain.get_main_net_txn()}
        return self.state, reward, done, info
