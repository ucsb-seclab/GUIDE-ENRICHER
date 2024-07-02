import random
from itertools import combinations


class Mutation:

    @staticmethod
    def generate_mutual_transactions(chain, wallet_list, mutable_address_range):
        for address in range(mutable_address_range[0], mutable_address_range[1]):
            chain.set_balance_of_addr(address, random.randint(100, 200))
            address_list = list(range(mutable_address_range[0], mutable_address_range[1]))
            combinations_list = list(combinations(address_list, 2))
            for from_addr, to_addr in combinations_list:
                if wallet_list.get(from_addr).get_balance() > 2:
                    wallet_list.get(from_addr).send_transaction(args={'to': to_addr, 'amount': 2})
