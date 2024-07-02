 #!/bin/bash

nohup python nova.py --name "dryrun-nova-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
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
  --no_iter 500 >dryrun2.log &
