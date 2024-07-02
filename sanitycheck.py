from Contract import TornadoCashContract
from Mainnet import EthMainnet
from Wallet import Wallet


def test1():
    chain = EthMainnet(5)
    tc = TornadoCashContract(chain)
    user = Wallet(chain=chain, wid=0, initial_money=1)
    user.send_transaction(contract=tc, function='deposit', args={'from': 1, 'to': 1})

    print('After Deposit')
    print("Chain:")
    eth_chain = chain.get_main_net_txn()
    print(eth_chain)
    print(eth_chain['args'].values)
    print('------')
    print('Contract:')
    tc_chain = tc._merkle_tree
    print(tc_chain)

    user.send_transaction(contract=tc, function='withdraw', args={'from': 1, 'to': 1})

    print('\n\nAfter withdraw')
    print("Chain:")
    eth_chain = chain.get_main_net_txn()
    print(eth_chain)
    print(eth_chain['args'].values)
    print('------')
    print('Contract:')
    tc_chain = tc._merkle_tree
    print(tc_chain)


if __name__ == '__main__':
    test1()
