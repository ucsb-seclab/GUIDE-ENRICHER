from flatbuffers.builder import np
from ray.rllib.algorithms.ppo import PPO


class LoadEvader:
    def __init__(self, checkpoint_path, config):
        self.config = config
        self.trainer = PPO(config=config)
        self.trainer.restore(checkpoint_path)

    def get_trainer(self):
        return self.trainer, self.config.get('agent_challenge_table')


class LoadEvaderTable:
    def __init__(self, configs):
        assert configs is not None
        self._table = {}
        index = 1
        for config in configs:
            self._table[index] = {
                'agent': LoadEvader(checkpoint_path=config.get('checkpoint_path'),
                                    config=config.get('config')),
                'is_done': False,
                'challenge_table': config.get('config').get('agent_challenge_table'),
                'addresses': list(range(config.get('config').get('agent_address_range_end'))),
                'observation': np.array([1, 0, 0, 0, 0, 0, 0, 0])
            }
            index += 1
        index = 0  # reset index
        self.address_next = 0
        self.address_map = {}
        for config in configs:
            _temp = {}
            for address in list(range(config.get('config').get('agent_address_range_end'))):
                _temp[address] = self.address_next
                self.address_next += 1
            self.address_map[index] = _temp
            index += 1

    def get_agent_table(self):
        return self._table

    def get_address_next(self):
        return self.address_map

    def get_mapped_address(self, agent_id, address_id):
        return self.address_map.get(agent_id).get(address_id)

    def get_crowd_address_starting_point(self):
        return self.address_next
