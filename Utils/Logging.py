import pandas as pd


class Log:
    def __init__(self):
        self.log_holder = []

    def add_evader_log(self, log):
        for fst_log, snd_log in log:
            status, action = fst_log
            temp = {'from': status[0],
                    'to': status[1],
                    'method': status[2],
                    'transaction': status[3],
                    'block': status[4],
                    'gas': status[5],
                    'action': action,
                    'reward': snd_log}
            self.log_holder.append(temp)

    def to_df(self):
        return pd.DataFrame(self.log_holder)
