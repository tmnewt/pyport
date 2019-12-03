import pandas as pd
import numpy as np

class Tracker(object):
    
    def __init__(self, initial_port_weights, df_log, date_start, initialize_end):
        self.initial_port_weights = initial_port_weights
        self.date_start = pd.to_datetime(date_start)
        self.initialize_end = pd.to_datetime(initialize_end)
        self.df_slice = df_log.loc[self.date_start : self.initialize_end]

        # for later
        self.temp_start_date = ''
        self.temp_end_date = ''
        self.temp_df_slice = ''
        self.last_date = ''
        
        self.holding_tracker_list = []
        self.complete_trading_returns = ''

        self.dates = list(self.df_slice.index.values)
        tracking_returns = []
        for date in self.dates:
            tracking_returns.append(np.dot(df_log.loc[date], self.initial_port_weights))
        
        tracking_returns = np.array(tracking_returns)
        tracking_returns[np.isnan(tracking_returns)] = 0
        self.initial_tracking_returns = tracking_returns + 1

    def add_new_period(new_period_start, new_period_end, new_df_log = None):
        if new_df_log is not None:
            self.temp_df_slice = new_df_log
        else
            self.temp_df_slice = self.df_slice
        
        pass
    
    def display_tracker_chart(self):
        pass

### Test
#df = pd.read_pickle('silly_strat_dataframe.pkl')
#df_log = np.log(df/ df.shift(1))




        


        