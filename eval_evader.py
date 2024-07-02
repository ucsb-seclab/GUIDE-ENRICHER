import os
import warnings

import pandas as pd
import ray
from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.algorithms.ppo import PPO

from Contract import TornadoCashContract, OtherContract
from Environments import TornadoCashGameEnvEvader, TornadoCashEvaderControlledEnv
from Mainnet import EthMainnet

warnings.filterwarnings("ignore")


def load(checkpoint_path, config):
    trainer = PPO(config=config)
    trainer.restore(checkpoint_path)
    return trainer


def evaluate(trainer, num_episodes, param):
    cum_rewards = []
    cum_steps = []
    for epi in range(num_episodes):
        chain = EthMainnet(5)
        tc = TornadoCashContract(chain)
        other = OtherContract(chain)
        env = TornadoCashEvaderControlledEnv(param, chain, tc, other)
        log = []
        episode_reward = 0
        obs = env.reset()
        done = False
        steps = 0
        while not done:
            action = trainer.compute_action(obs)
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            steps += 1
            log.append({'game': epi, 'txn': info.get('txn'), 'episode': epi, 'step': steps, 'observation': obs,
                        'action': action,
                        'reward': reward})
        cum_steps.append(steps)
        cum_rewards.append(episode_reward)
        pd.DataFrame(log).to_csv(f'/data/ravindu/data/new/row3/log-{epi}-{episode_reward}.csv', index=False)
        # env.chain.get_main_net_txn().to_csv(f'/data/ravindu/data/new/row1/chain-{epi}-{episode_reward}.csv',
        #                                     index=False)
        print(f"Game: {epi}/{num_episodes}", "Steps performed : ", steps, "Episode reward:", episode_reward)
    avg_reward = sum(cum_rewards) / num_episodes
    print('FINAL REWARD : ', avg_reward)
    return cum_rewards, cum_steps


class CustomCallbackEvader(DefaultCallbacks):

    def on_episode_step(self, *, worker, base_env, episode, **kwargs):
        pass

    def on_episode_end(self, *, worker, base_env, policies, episode, **kwargs):
        pass


if __name__ == '__main__':
    config = {
        "env": TornadoCashGameEnvEvader,
        "num_workers": 1,
        "horizon": 10000,
        "env_config": {
            'block_size': 5,
            'max_wait_time': 5,
            'no_addresses_agent_challenge_table': 2,
            'agent_challenge_table': [30, 30],
            'agent_address_range_starts': 0,
            'agent_address_range_end': 250,
            'agent_mutable_address_range_start': 10,
            'agent_mutable_address_range_end': 20,
            'crowd_address_range_starts': 250,
            'no_of_crowd': 200,
            'no_of_wallets_for_each_crowd_agent': 100,
            'amount_of_money_in_each_crowd': 100
        },
        "model": {
            # "custom_model": "model_with_batch_normalization"
            "fcnet_hiddens": [64, 64],
        },
        "callbacks": CustomCallbackEvader,
        "framework": "tf",
    }

    _param = {
        'block_size': 5,
        'max_wait_time': 5,
        'no_addresses_agent_challenge_table': 2,
        'agent_challenge_table': [30, 30],
        'agent_address_range_starts': 0,
        'agent_address_range_end': 250,
        'agent_mutable_address_range_start': 10,
        'agent_mutable_address_range_end': 20,
        'crowd_address_range_starts': 250,
        'no_of_crowd': 200,
        'no_of_wallets_for_each_crowd_agent': 100,
        'amount_of_money_in_each_crowd': 100
    }
    os.environ["TMPDIR"] = '/data/ravindu/temp_ray'
    os.environ["CUDA_VISIBLE_DEVICES"] = "3"

    ray.init()

    model = load(
        '/data/ravindu/evader/check_point/Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-2-with-10-2023-07-04_00-57-17/checkpoint_000998',
        config)

    eval_result = evaluate(model, 500, _param)

    pd.DataFrame({'reward': eval_result[0], 'steps': eval_result[1]}).to_csv('row3.csv',
                                                                             index=False)

    ray.shutdown()
