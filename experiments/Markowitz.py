#from findatapy.util import SwimPool; SwimPool()
#from findatapy.market import Market, MarketDataRequest, MarketDataGenerator
import pandas as pd, numpy as np, scipy.optimize as sciop
import matplotlib.pyplot as plt
#from datetime import timedelta
#import datetime

#import pandas_datareader as pdr

# class and experiments in the same file...

# when and where should the code handle different observation frequency?
# it would be nice to flip a switch (not literally...) and alter time frames, observation frequencies, etc, for a portfolio.

# thinking that should go somewhere else. 
# but I'd like a feature that catch when the user enters a observation frequence that doesn't make sense given the data.
# ahhh, so many choices to make.

class Markowitz(object):
    def __init__(self, df_log_returns, observation_start, observation_end , freq_of_obser):
        self.df_log_returns = df_log_returns
        self.observation_start = observation_start
        self.observation_end = observation_end
        self.frequency_of_observations = freq_of_obser
        
        # additional attributes.
        self.mean_returns = df_log_returns[observation_start:observation_end].mean()
        self.num_tickers = len(list(df_log_returns.columns.values))
        self.weights = self.num_tickers * [1. /self.num_tickers]
        #opt = sciop.minimize()


    def max_sharpe_ratio(self):
        pass






#df = pd.read_pickle('silly_strat_dataframe.pkl')
#df_log = np.log(df/ df.shift(1))
#number_comp = len(list(df_log.columns.values))
#weight_temp = number_comp * [1. / number_comp,]
#print(weight_temp)
#
#port = Markowitz(df_log, '2015', '2016', 252)
#print(port.df_log_returns)
#print(port.frequency_of_observations)
#print(port.mean_returns)
#print(port.num_tickers)
#print(port.weights)



    
    






