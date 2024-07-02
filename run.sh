#!/bin/bash

echo "############################################################################"
echo "| Challenge  Starting...|"
echo "############################################################################"

nohup python nova.py --name "nova-dry-run-" \
  --data_dir "/data/ravindu/evader/data/" \
  --log_dir "/data/ravindu/evader/log/" \
  --checkpoint_dir "/data/ravindu/evader/check_point/" \
  --no_addresses_agent_challenge_table 2 \
  --agent_challenge_table "[2,3]" \
  --agent_address_range_starts 0 \
  --agent_address_range_end 1000 \
  --agent_mutable_address_range_start 10 \
  --agent_mutable_address_range_end 20 \
  --crowd_address_range_starts 1000 \
  --no_of_crowd 250 \
  --no_of_wallets_for_each_crowd_agent 100 \
  --amount_of_money_in_each_crowd 100 \
  --fcnet_hiddens "[64, 64]" \
  --no_iter 500 > crowd-test.log &

#echo "############################################################################"
#echo "| Challenge  Starting...|"
#echo "############################################################################"
#
#sleep 10
#
nohup python evader.py --name "scale-test-" \
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
  --fcnet_hiddens "[128, 128]" \
  --no_iter 500 >fcnet_hiddens_scale_by2.log &
#
#echo "############################################################################"
#echo "| Challenge  Starting...|"
#echo "############################################################################"
#
#sleep 10
#
#nohup python evader.py --name "fcnet_hiddens_scale_by4-" \
#  --data_dir "/data/ravindu/evader/data/" \
#  --log_dir "/data/ravindu/evader/log/" \
#  --checkpoint_dir "/data/ravindu/evader/check_point/" \
#  --no_addresses_agent_challenge_table 3 \
#  --agent_challenge_table "[3,3,3]" \
#  --agent_address_range_starts 0 \
#  --agent_address_range_end 250 \
#  --agent_mutable_address_range_start 10 \
#  --agent_mutable_address_range_end 20 \
#  --crowd_address_range_starts 250 \
#  --no_of_crowd 200 \
#  --no_of_wallets_for_each_crowd_agent 100 \
#  --amount_of_money_in_each_crowd 100 \
#  --fcnet_hiddens "[256, 256]" \
#  --no_iter 500 >fcnet_hiddens_scale_by4.log &
#
#echo "############################################################################"
#echo "| Challenge  Starting...|"
#echo "############################################################################"
#
#sleep 10
#
#nohup python evader.py --name "fcnet_hiddens_length_3-" \
#  --data_dir "/data/ravindu/evader/data/" \
#  --log_dir "/data/ravindu/evader/log/" \
#  --checkpoint_dir "/data/ravindu/evader/check_point/" \
#  --no_addresses_agent_challenge_table 3 \
#  --agent_challenge_table "[3,3,3]" \
#  --agent_address_range_starts 0 \
#  --agent_address_range_end 250 \
#  --agent_mutable_address_range_start 10 \
#  --agent_mutable_address_range_end 20 \
#  --crowd_address_range_starts 250 \
#  --no_of_crowd 200 \
#  --no_of_wallets_for_each_crowd_agent 100 \
#  --amount_of_money_in_each_crowd 100 \
#  --fcnet_hiddens "[64, 64, 64]" \
#  --no_iter 500 >fcnet_hiddens_length_3.log &
#
#echo "############################################################################"
#echo "| Challenge  Starting...|"
#echo "############################################################################"
#
#sleep 10
#
#nohup python evader.py --name "fcnet_hiddens_length_4-" \
#  --data_dir "/data/ravindu/evader/data/" \
#  --log_dir "/data/ravindu/evader/log/" \
#  --checkpoint_dir "/data/ravindu/evader/check_point/" \
#  --no_addresses_agent_challenge_table 3 \
#  --agent_challenge_table "[3,3,3]" \
#  --agent_address_range_starts 0 \
#  --agent_address_range_end 250 \
#  --agent_mutable_address_range_start 10 \
#  --agent_mutable_address_range_end 20 \
#  --crowd_address_range_starts 250 \
#  --no_of_crowd 200 \
#  --no_of_wallets_for_each_crowd_agent 100 \
#  --amount_of_money_in_each_crowd 100 \
#  --fcnet_hiddens "[64, 64, 64, 64]" \
#  --no_iter 500 >fcnet_hiddens_length_4.log &
