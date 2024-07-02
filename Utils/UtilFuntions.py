import numpy as np
import pandas as pd

from Wallet import Wallet


class Util:
    @staticmethod
    def slice(df, start, end, slice_size):
        tdf = df.iloc[start:end, :][['from', 'to', 'method', 'transaction', 'block', 'gas']]
        tdf = tdf.iloc[:, :]  # will remove after check
        if tdf.shape[0] < slice_size:
            zeros_df = pd.DataFrame(np.full((slice_size - tdf.shape[0], tdf.shape[1]), -10), columns=tdf.columns)
            tdf = pd.concat([tdf, zeros_df], axis=0)
        tdf.loc[tdf['from'] == 'TC', 'from'] = -1
        tdf.loc[tdf['from'] == 'OTHER', 'from'] = -2
        tdf.loc[tdf['to'] == 'TC', 'to'] = -1
        tdf.loc[tdf['to'] == 'OTHER', 'to'] = -2
        tdf.loc[tdf['method'] == 'transfer', 'method'] = 0
        tdf.loc[tdf['method'] == 'deposit', 'method'] = 1
        tdf.loc[tdf['method'] == 'withdraw', 'method'] = 2
        tdf.loc[tdf['method'] == 'internal', 'method'] = 3
        return tdf.to_numpy()

    @staticmethod
    def check(address, evader_address_range):
        start, end = evader_address_range
        return address in list(range(start, end))

    @staticmethod
    def generate_wallets(chain, challenge_table, total_addresses):
        _money_in_list = challenge_table + [0] * (total_addresses - len(challenge_table))
        _data = {}
        for index in range(len(_money_in_list)):
            _data[index] = Wallet(chain=chain, wid=index, initial_money=_money_in_list[index])
        return _data
