import pandas as pd


class Tutela:

    def __init__(self, chain, contract):
        self.HISTORY = pd.DataFrame(columns=['txn', 'heuristic1', 'heuristic2', 'heuristic3', 'heuristic4'])
        self.chain = chain
        self.contract = contract

    def txn_map(self):
        eth_chain_snap_shot = self.chain.get_main_net_txn()
        last_aget_transaction = eth_chain_snap_shot.iloc[-1]
        if last_aget_transaction.method == 'deposit':
            return eth_chain_snap_shot.iloc[-1:].txn.tolist()
        if last_aget_transaction.method == 'internal':
            return eth_chain_snap_shot.iloc[-2:].txn.tolist()

    def heuristic1(self):
        eth_chain_snap_shot = self.chain.get_main_net_txn()
        last_aget_transaction = eth_chain_snap_shot.iloc[-1]
        _is_detected = []

        if last_aget_transaction.method == 'deposit' and ((eth_chain_snap_shot.loc[
                                                               (eth_chain_snap_shot['to'] == 'TC') & (
                                                                       eth_chain_snap_shot['from'] ==
                                                                       last_aget_transaction['from']) & (
                                                                       eth_chain_snap_shot[
                                                                           'method'] == 'withdraw')].shape[0] > 0) or (
                                                                  eth_chain_snap_shot.loc[
                                                                      (eth_chain_snap_shot['from'] == 'TC') & (
                                                                              eth_chain_snap_shot['to'] ==
                                                                              last_aget_transaction['from']) & (
                                                                              eth_chain_snap_shot[
                                                                                  'method'] == 'internal')].shape[
                                                                      0] > 0)):
            _is_detected.append(True)

        elif last_aget_transaction.method == 'internal':
            _last_before_aget_transaction = eth_chain_snap_shot.iloc[-2]
            if _last_before_aget_transaction.method == 'withdraw' and eth_chain_snap_shot.loc[
                (eth_chain_snap_shot['to'] == 'TC') & (
                        eth_chain_snap_shot['from'] == _last_before_aget_transaction['from']) & (
                        eth_chain_snap_shot['method'] == 'deposit')].shape[0] > 0:
                _is_detected.append(True)
            else:
                _is_detected.append(False)
            if last_aget_transaction.method == 'internal' and eth_chain_snap_shot.loc[
                (eth_chain_snap_shot['to'] == 'TC') & (eth_chain_snap_shot['from'] == last_aget_transaction['to']) & (
                        eth_chain_snap_shot['method'] == 'deposit')].shape[0] > 0:
                _is_detected.append(True)
            else:
                _is_detected.append(False)
        else:
            _is_detected = [False]

        return _is_detected

    def heuristic2(self):
        eth_chain_snap_shot = self.chain.get_main_net_txn()
        last_aget_transaction = eth_chain_snap_shot.iloc[-1]
        _is_detected = []
        if last_aget_transaction.method == 'internal':
            _last_before_aget_transaction = eth_chain_snap_shot.iloc[-2]
            if _last_before_aget_transaction.method == 'withdraw' and eth_chain_snap_shot.loc[
                (eth_chain_snap_shot['to'] == 'TC') & (eth_chain_snap_shot['method'] == 'deposit') & (
                        eth_chain_snap_shot['gas'] == _last_before_aget_transaction['gas'])].shape[0] == 1:
                _is_detected.append(True)
            else:
                _is_detected.append(False)
            if last_aget_transaction.method == 'internal' and eth_chain_snap_shot.loc[
                (eth_chain_snap_shot['to'] == 'TC') & (eth_chain_snap_shot['method'] == 'deposit') & (
                        eth_chain_snap_shot['gas'] == last_aget_transaction['gas'])].shape[0] == 1:
                _is_detected.append(True)
            else:
                _is_detected.append(False)
        else:
            _is_detected = [False]

        return _is_detected

    def heuristic3(self):
        eth_chain_snap_shot = self.chain.get_main_net_txn()
        last_aget_transaction = eth_chain_snap_shot.iloc[-1]
        _is_detected = []
        deposit_history = set(eth_chain_snap_shot.loc[
                                  (eth_chain_snap_shot['to'] == 'TC') & (eth_chain_snap_shot['method'] == 'deposit')][
                                  'from'].tolist())
        if last_aget_transaction.method == 'internal':
            _last_before_aget_transaction = eth_chain_snap_shot.iloc[-2]
            if _last_before_aget_transaction.method == 'withdraw':
                check = False
                for addr in deposit_history:
                    if eth_chain_snap_shot.loc[((eth_chain_snap_shot['from'] == _last_before_aget_transaction[
                        'from']) & (eth_chain_snap_shot['to'] == addr)) | ((eth_chain_snap_shot['from'] == addr) & (
                            eth_chain_snap_shot['to'] == _last_before_aget_transaction['from']))].shape[0] > 0:
                        check = True
                        break
                if check:
                    _is_detected.append(True)
                else:
                    _is_detected.append(False)
            if last_aget_transaction.method == 'internal':
                check = False
                for addr in deposit_history:
                    if eth_chain_snap_shot.loc[((eth_chain_snap_shot['from'] == last_aget_transaction['to']) & (
                            eth_chain_snap_shot['to'] == addr)) | ((eth_chain_snap_shot['from'] == addr) & (
                            eth_chain_snap_shot['to'] == last_aget_transaction['to']))].shape[0] > 0:
                        check = True
                        break
                if check:
                    _is_detected.append(True)
                else:
                    _is_detected.append(False)
        else:
            _is_detected = [False]

        return _is_detected

    def heuristic4(self):
        eth_chain_snap_shot = self.chain.get_main_net_txn()
        last_aget_transaction = eth_chain_snap_shot.iloc[-1]
        _is_detected = []
        if last_aget_transaction.method == 'internal':
            _last_before_aget_transaction = eth_chain_snap_shot.iloc[-2]
            note_hash = _last_before_aget_transaction['args'].get('note hash')
            origin_block_of_note = self.contract.get_origin_block_of_note(note_hash)
            origin_block = self.chain.get_current_block(origin_block_of_note)
            no_of_deposit_in_origin_block = origin_block.loc[origin_block['method'] == 'deposit'].shape[0]
            if _last_before_aget_transaction.method == 'withdraw' and no_of_deposit_in_origin_block == 1:
                _is_detected = [True, True]
            else:
                _is_detected = [False, False]
        else:
            _is_detected = [False]

        return _is_detected

    def heuristic5(self):
        pass

    def get_step_heuristic_reward_history(self):
        return self.HISTORY

    def run_tutela_heuristics_check(self):
        heuristic1 = self.heuristic1()
        heuristic2 = self.heuristic2()
        heuristic3 = self.heuristic3()
        heuristic4 = self.heuristic4()
        txn = self.txn_map()
        assert len(heuristic1) == len(heuristic2), 'h1 {}\th2 {}'.format(len(heuristic1), len(heuristic2))
        for _txn, hur1, hur2, hur3, hur4 in zip(txn, heuristic1, heuristic2, heuristic3, heuristic4):
            self.HISTORY = pd.concat([self.HISTORY, pd.DataFrame(
                [{'txn': _txn, 'heuristic1': hur1, 'heuristic2': hur2, 'heuristic3': hur3,
                  'heuristic4': hur4}])]).reset_index(
                drop=True)

        return all(heuristic1) and all(heuristic2) and all(heuristic3) and all(heuristic4)

    def run_nova_heuristics_check(self):
        return self.run_tutela_heuristics_check()
