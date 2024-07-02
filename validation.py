from Contract import TornadoCashContract, OtherContract
from Mainnet import EthMainnet
from Wallet import Wallet
from tqdm import tqdm


def verifier():
    mapper = {}

    _x = []

    seq = list(map(lambda x: x.split(','), open('data.txt').read().split('\n')))
    data = set(tuple(map(lambda x: x[1], seq)))

    print(len(seq))

    main_net = EthMainnet(5)
    tc = TornadoCashContract(chain=main_net)

    main_net.main_net_balance['TC'] = 0

    # print(main_net.main_net_balance['TC'])

    for addr in tqdm(data):
        # print(addr)
        mapper[addr] = Wallet(chain=main_net, wid=addr, initial_money=100)
        # print(mapper.get(addr).get_balance())
        # break

    for event, addr in tqdm(seq):
        if event == 'deposit':
            mapper[addr].send_transaction(tc, 'deposit', {'t': addr})
        if event == 'withdraw':
            mapper[addr].send_transaction(tc, 'withdraw', {'t': addr})

        _x.append(main_net.main_net_balance['TC'])
    print(main_net.main_net_balance['TC'])


if __name__ == '__main__':
    verifier()
