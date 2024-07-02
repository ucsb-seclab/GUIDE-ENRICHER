nohup python evader.py --name "exp1-group-1-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 3 \
  --agent_challenge_table "[3,3,3]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 200 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[32, 32]" \
  --no_iter 500 >exp1-group-1.log &


nohup python evader.py --name "exp1-group-2-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 3 \
  --agent_challenge_table "[3,3,3]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 200 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[32, 32]" \
  --no_iter 500 >exp1-group-2.log &


nohup python evader.py --name "exp1-group-3-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 3 \
  --agent_challenge_table "[3,3,3]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 200 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[32, 32]" \
  --no_iter 500 >exp1-group-3.log &

nohup python evader.py --name "exp1-group-4-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 3 \
  --agent_challenge_table "[3,3,3]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 200 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[32, 32]" \
  --no_iter 500 >exp1-group-4.log &