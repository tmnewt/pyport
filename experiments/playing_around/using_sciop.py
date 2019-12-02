import pandas as pd, numpy as np, scipy.optimize as sciop
import matplotlib.pyplot as plt

# figure out how to correctly use the sciop.minimize method correctly by passing *args.

# generate an array of expected returns.
df = pd.read_pickle('silly_strat_dataframe.pkl')
df_log_returns = np.log(df/ df.shift(1))

df_slice = df_log_returns.loc['2015' : '2016']
mean_ret = df_slice.mean()
print(mean_ret)


def portfolio_statistics(weights, mean_returns, frame):
    weight_array = np.array(weights)
    portfolio_return = np.sum(mean_returns * weight_array)*252
    portfolio_vol = np.sqrt(np.dot(weight_array.T, np.dot(frame.cov()* 252, weight_array)))
    sharpe_ratio = portfolio_return / portfolio_vol 
    return np.array([portfolio_return, portfolio_vol, sharpe_ratio])

def max_sharpe_ratio(weights, expected_returns, frame):
    return -portfolio_statistics(weights, expected_returns, frame)[2]

number_comp = len(list(df_log_returns.columns.values))
weight_guess = number_comp * [1. / number_comp,]
cons = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
bnds = tuple((0,1) for x in range(number_comp)) 
extra_args = mean_ret, df_slice
optimize = sciop.minimize(max_sharpe_ratio,
                      weight_guess,
                      args= extra_args,
                      method = 'SLSQP',
                      bounds= bnds,
                      constraints = cons)

print(optimize['x'].round(3))

