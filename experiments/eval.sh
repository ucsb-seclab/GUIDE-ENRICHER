#!/bin/bash

echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-1 Starting...|"
echo "############################################################################"

nohup python evader.py --name "Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-1-with-10-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 1 \
  --agent_challenge_table "[30]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 200 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[64, 64]" \
  --no_iter 500 >Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-1-with-10.log &

echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-1 Started...|"
echo "############################################################################"
sleep 10
echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-2 Starting...|"
echo "############################################################################"

nohup python evader.py --name "Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-2-with-100-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 2 \
  --agent_challenge_table "[300,300]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 750 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 750 \
  --no_of_crowd 500 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[64, 64]" \
  --no_iter 2000 >Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-2-with-100.log &

echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-2 Started...|"
echo "############################################################################"
sleep 10
echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-3 Starting...|"
echo "############################################################################"

nohup python evader.py --name "Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-3-with-10-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 3 \
  --agent_challenge_table "[30,30,30]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 200 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[64, 64]" \
  --no_iter 1500 >Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-3-with-10.log &

echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-3 Started...|"
echo "############################################################################"
sleep 10
echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-4 Starting...|"
echo "############################################################################"

nohup python evader.py --name "Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-4-with-10-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 4 \
  --agent_challenge_table "[30,30,30,30]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 200 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[64, 64]" \
  --no_iter 2000 >Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-4-with-10.log &

echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-4 Started...|"
echo "############################################################################"
sleep 10
echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-5 Starting...|"
echo "############################################################################"

nohup python evader.py --name "Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-5-with-10-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 5 \
  --agent_challenge_table "[30,30,30,30,30]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 250 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 250 \
  --no_of_crowd 200 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[64, 64]" \
  --no_iter 2000 >Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-5-with-10.log &

echo "############################################################################"
echo "| Challenge-Table-Length-Uniform-Eth-distribution-Test-Length-5 Started...|"
echo "############################################################################"
