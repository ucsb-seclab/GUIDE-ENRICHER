import glob
import os
import time
import warnings
from datetime import datetime

# import gymnasium as gym # for env Ray version: 2.4.0
import ray
# from ray.rllib.agents.ppo import PPOTrainer  # Ray version: 2.0.0
from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.algorithms.ppo import PPO  # for env Ray version: 2.4.0
from tqdm import tqdm

from Environments import TornadoCashGameEnvEvader, TornadoCashGameEnvDetector

warnings.filterwarnings("ignore")


class CustomCallback(DefaultCallbacks):

    def on_episode_end(self, *, worker, base_env, policies, episode, **kwargs):
        chain = episode.last_info_for().get('chain')
        chain.to_csv(f'{data_log_dir}/{episode.episode_id}.eth', index=False)
        # st
        # eps = episode.last_info_for().get('log')
        # steps.to_csv(f'{data_log_dir}/{episode.episode_id}.steps', index=False)
        pass


class CustomCallbackEvader(DefaultCallbacks):

    def on_episode_step(self, *, worker, base_env, episode, **kwargs):
        pass

    def on_episode_end(self, *, worker, base_env, policies, episode, **kwargs):
        pass


class RunGame:
    @staticmethod
    def load_ppo_trainer(config):
        trainer = PPO(config=config)  # for env Ray version: 2.4.0
        # trainer = PPOTrainer(config=config)  # for env Ray version: 2.0.0
        return trainer

    @staticmethod
    def run_iteratively(no_iter_in, log_dir_in=None, data_log_dir_in=None, checkpoint_dir=None, config=None):
        os.environ["TMPDIR"] = '/data/ravindu/temp_ray'
        os.environ["CUDA_VISIBLE_DEVICES"] = "3"
        ray.init()
        trainer = RunGame.load_ppo_trainer(config=config)

        result_file = open(f'{log_dir_in}/dryrun.csv', 'a')
        result_file.write("episode_reward_mean,episode_reward_max,episode_reward_min\n")
        result_file.flush()

        log_eth = open(f'{log_dir_in}/eth.log', 'w')
        log_step = open(f'{log_dir_in}/step.log', 'w')

        pre_eth = []
        pre_step = []

        for _i in tqdm(range(no_iter_in)):
            train = trainer.train()

            trainer.save(checkpoint_dir)

            episode_reward_mean = train['episode_reward_mean']
            episode_reward_max = train['episode_reward_max']
            episode_reward_min = train['episode_reward_min']
            print(
                f'episode_reward_mean :{episode_reward_mean}\tepisode_reward_max :{episode_reward_max}\t'
                f'episode_reward_min :{episode_reward_min}')

            result_file.write(f'{episode_reward_mean},{episode_reward_max},{episode_reward_min}\n')
            result_file.flush()

            files_eth = glob.glob(f'{data_log_dir_in}/*.eth')
            files_step = glob.glob(f'{data_log_dir_in}/*.steps')

            files_eth.sort(key=os.path.getmtime)
            log_eth.write(f'{",".join(list(filter(lambda x: x not in pre_eth, files_eth)))}\n')
            log_eth.flush()
            pre_eth = files_eth

            files_step.sort(key=os.path.getmtime)
            log_step.write(f'{",".join(list(filter(lambda x: x not in pre_step, files_step)))}\n')
            log_step.flush()
            pre_step = files_step

        result_file.flush()
        result_file.close()

        log_eth.flush()
        log_eth.close()

        log_step.flush()
        log_step.close()

        ray.shutdown()


if __name__ == '__main__':
    # 3. debug

    start_time = time.time()

    DETECTOR_DATA_LOG_DIR = "/data/ravindu/detector/data/"
    DETECTOR_LOG_DIR = "/data/ravindu/detector/log/"
    DETECTOR_CHECK_POINT_DIR = "/data/ravindu/detector/check_point/"
    TEST_NAME = "detector-"

    current_datetime = datetime.now()
    folder_name = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    data_log_dir = f'{DETECTOR_DATA_LOG_DIR}{TEST_NAME}{folder_name}'
    log_dir = f'{DETECTOR_LOG_DIR}{TEST_NAME}{folder_name}'
    check_point_dir = f'{DETECTOR_CHECK_POINT_DIR}{TEST_NAME}{folder_name}'

    os.mkdir(data_log_dir)
    os.mkdir(log_dir)
    os.mkdir(check_point_dir)

    detector_config = {
        "env": TornadoCashGameEnvDetector,
        "num_workers": 1,
        "horizon": 10000,
        "env_config": {
            'window_size': 1,
            'block_size': 5,
            'evader_check_point_path': '/data/ravindu/evader/check_point/Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-3-2023-06-19_17-51-03/checkpoint_000496',
            'evader_configs': {
                "env": TornadoCashGameEnvEvader,
                "num_workers": 1,
                "horizon": 10000,
                "env_config": {
                    'block_size': 5,
                    'max_wait_time': 5,
                    'no_addresses_agent_challenge_table': 3,
                    'agent_challenge_table': [3, 3, 3],
                    'agent_address_range_starts': 0,
                    'agent_address_range_end': 60,
                    'agent_mutable_address_range_start': 10,
                    'agent_mutable_address_range_end': 20,
                    'crowd_address_range_starts': 60,
                    'no_of_crowd': 100,
                    'no_of_wallets_for_each_crowd_agent': 100,
                    'amount_of_money_in_each_crowd': 100
                },
                "model": {
                    # "custom_model": "model_with_batch_normalization"
                    "fcnet_hiddens": [64, 64],
                },
                "callbacks": CustomCallbackEvader,
                "framework": "tf",
            },
            'evader_env_configs': {
                'block_size': 5,
                'max_wait_time': 5,
                'no_addresses_agent_challenge_table': 3,
                'agent_challenge_table': [3, 3, 3],
                'agent_address_range_starts': 0,
                'agent_address_range_end': 60,
                'agent_mutable_address_range_start': 10,
                'agent_mutable_address_range_end': 20,
                'crowd_address_range_starts': 60,
                'no_of_crowd': 100,
                'no_of_wallets_for_each_crowd_agent': 100,
                'amount_of_money_in_each_crowd': 100
            },
        },
        "model": {
            # "custom_model": "model_with_batch_normalization"
            "fcnet_hiddens": [64, 64],
        },
        "callbacks": CustomCallback,
        "framework": "tf",
    }

    no_iter = 50
    RunGame.run_iteratively(log_dir_in=log_dir, data_log_dir_in=data_log_dir, checkpoint_dir=check_point_dir,
                            no_iter_in=no_iter, config=detector_config)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken: {execution_time} seconds")
    # End!!
