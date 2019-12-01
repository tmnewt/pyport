
import pandas as pd, numpy as np, scipy.optimize as sciop
#import matplotlib.pyplot as plt

class Markowitz(object):
    def __init__(self, df_log_returns, observation_start, observation_end , freq_of_observations, can_short = False):
        self.df_log_returns = df_log_returns
        self.observation_start = observation_start
        self.observation_end = observation_end
        self.frequency_of_observations = freq_of_observations
        self.can_short = can_short
        
        # Tickers in this portfolio
        self.tickers = list(self.df_log_returns.columns.values)

        # additional attributes and calculations
        self.df_slice =  self.df_log_returns[self.observation_start : self.observation_end]
        self.mean_returns = self.df_slice.mean()
        
        self.num_tickers = len(self.tickers)
        weight_guess = self.num_tickers * [1. /self.num_tickers]

        self.cov_frame = self.df_slice.cov() * self.frequency_of_observations

        # Handling shorts
        if self.can_short:
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
            bnds = tuple((-0.1,1) for x in range(self.num_tickers)) 
        else:
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
            bnds = tuple((0,1) for x in range(self.num_tickers)) 

        opt = sciop.minimize(self.max_sharpe_ratio,
                      weight_guess,
                      method = 'SLSQP',
                      bounds= bnds,
                      constraints = cons)
        
        self.portfolio_allocation = opt['x'].round(3)
        
        ticker_dictionary = {}
        for i in range(self.num_tickers):
            ticker_dictionary[self.tickers[i]] = self.portfolio_allocation[i]


        self.allocation_by_ticker = ticker_dictionary


    def max_sharpe_ratio(self, weights):
        weight_array = np.array(weights)
        self.portfolio_return = np.sum(self.mean_returns * weight_array) * self.frequency_of_observations
        self.portfolio_volatility = np.sqrt(np.dot(weight_array.T,
                                                    np.dot(self.cov_frame, 
                                                            weight_array)))
        sharp_ratio = self.portfolio_return / self.portfolio_volatility
        self.sharp_ratio = sharp_ratio
        return -sharp_ratio

    def display_portfolio_statistics(self):
        print('Expected Portfolio Return')







df = pd.read_pickle('silly_strat_dataframe.pkl')
df_log = np.log(df/ df.shift(1))
print(df_log)


#
port = Markowitz(df_log, '2015', '2016', 252, can_short=True)
print(port.can_short)
print(port.tickers)
print(port.portfolio_return)
print(port.portfolio_volatility)
print(port.sharp_ratio)
print(port.portfolio_allocation)

print(port.allocation_by_ticker)

    
    






