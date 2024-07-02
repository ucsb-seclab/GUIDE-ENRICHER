import warnings

# import gymnasium as gym # for env Ray version: 2.4.0
from ray.rllib.algorithms.ppo import PPO

warnings.filterwarnings("ignore")


class LoadEvader:
    def __init__(self, checkpoint_path, config):
        self.config = config
        self.trainer = PPO(config=self.config)
        self.trainer.restore(checkpoint_path)
        self.obs = None
        self.reward = 0
        self.done = False
        self.info = None

    def get_ppo_trainer(self):
        return self.trainer

    def get_obs(self):
        return self.obs

    def set_obs(self, obs):
        self.obs = obs

    def get_reward(self):
        return self.reward

    def set_reward(self, reward):
        self.reward = reward

    def is_done(self):
        return self.done

    def set_don(self, done):
        self.done = done

    def get_info(self):
        return self.info

    def set_info(self, info):
        self.info = info
