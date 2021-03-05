from pandas import DataFrame

class Markowitz:
    def __init__(self, ts_df:DataFrame):
        self.ts_df = ts_df

        self.tickers = list(self.ts_df.columns.values)