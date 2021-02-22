import pandas as pd
import numpy as np
from markowitz import Markowitz

class Tracker(object):
    
    def __init__(self, initial_port_weights, df_log_return, initial_start, initial_end):
        self.initial_port_weights = initial_port_weights
        self.initial_start = pd.to_datetime(initial_start)
        self.initial_end = pd.to_datetime(initial_end)
        self.initial_df_slice = df_log_return.loc[self.initial_start : self.initial_end]

        # for later
        self.temp_start_date = ''
        self.temp_end_date = ''
        self.temp_df_slice = ''
        self.last_date = ''
        
        self.holding_tracker_list = []
        self.complete_tracking_returns = []

        self.initial_dates = list(self.initial_df_slice.index.values)
        tracking_returns = [np.dot(df_log_return.loc[date], self.initial_port_weights) for date in self.initial_dates]
        #for date in self.initial_dates:
        #    tracking_returns.append(np.dot(df_log_return.loc[date], self.initial_port_weights))
        
        tracking_returns = np.array(tracking_returns)
        tracking_returns[np.isnan(tracking_returns)] = 0
        self.initial_tracking_returns = tracking_returns + 1
        self.holding_tracker_list.append(self.initial_tracking_returns)

    def add_tracker_period(self, new_period_weights, new_period_start, new_period_end, new_df_log = None):
        if new_df_log is not None:
            temp_df_slice = new_df_log
        else:
            temp_df_slice = self.initial_df_slice[new_period_start : new_period_end]
        
        temp_dates = list(temp_df_slice.index.values)
        new_period_tracking_returns = [np.dot(temp_df_slice.loc[date], new_period_weights) for date in temp_dates]  

        self.holding_tracker_list.append(new_period_tracking_returns)

        
    def remove_tracker_period(self):
        pass

    def display_tracker_chart(self):
        pass

    def display_tracker_actions(self):
        pass

### Test
df = pd.read_pickle('silly_strat_dataframe.pkl')
df_log = np.log(df/ df.shift(1))

port = Markowitz(df_log, '2015', '2015-12-31', 252)

tracking = Tracker(port.allocate_weights(), df_log, '2016', '2016-03-31')
print(tracking.initial_start)
print(tracking.initial_end)
print(tracking.initial_tracking_returns)



        


        