# GUIDE-ENRICHER

### Description
This repository contains the code and model for the GuideEnricher: Protecting the Anonymity of Ethereum Mixing Service Users with Deep Reinforcement Learning. Read the full paper [USENIX 24]().

### Requirements
GuideEnricher requires Python 3.8 or later. You can install the required packages by running: `conda create --name <env> --file conda_requirements.txt`

Note: GuideEnricher is developed on `ray 2.0.0` and `tensorflow 2.10.0`

### Retrain the game
To retrain the game, you can use the following command:
```
python evader.py --name "<name of your experiment>" \
  --data_dir "<>" \
  --log_dir "<>" \
  --checkpoint_dir "<>" \
  --no_addresses_agent_challenge_table 2 \
  --agent_challenge_table "[2,3]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 50 \
  --no_of_wallets_for_each_crowd_agent 50 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[32, 32]" \
  --no_iter 500
  ```
You can modify the parameters as your game. eg: ```agent_challenge_table, agent_address_range_starts, agent_address_range_end, agent_mutable_address_range_start, agent_mutable_address_range_end, crowd_address_range_starts, no_of_crowd, no_of_wallets_for_each_crowd_agent, amount_of_money_in_each_crowd, fcnet_hiddens, no_iter.```

### Run the pretrained game
To run the pretrained game, load the agent's model and config (check `model` dir), and run :
```python eval_evader.py```   


#### Extended Appendix
Read the extended appendix: [here](docs/GuideEnricher_Extended_Appendix.pdf)
