from Wallet import Wallet


class NovaUserProvisioning:
    def __init__(self, chain, address_range_starts, address_range_end, _money_in_list):
        _money_in_list = _money_in_list + [0] * (address_range_end - len(_money_in_list))
        self.wallets = {key: Wallet(chain=chain, wid=key, initial_money=money) for key, money in
                        zip(list(range(address_range_starts, address_range_end)), _money_in_list)}
        self.wallets_addresses = list(self.wallets.keys())
        self.notes = []

    def set_note(self, note):
        self.notes.append(note)

    def remove_note(self, note):
        if note['fund'] == 0:
            self.notes.remove(note)

    def get_notes(self):
        return self.notes

    def get_total_no_of_notes(self):
        return len(self.notes)

    def get_wallets(self):
        return self.wallets

    def get_wallets_addresses(self):
        return self.wallets_addresses
