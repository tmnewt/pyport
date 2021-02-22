# See book, Python for Finance by Yves Hilpisch - Chapter 11

import pandas as pd, numpy as np, scipy.optimize as sciop, sys
import matplotlib.pyplot as plt
from mytools import ask_to_display


df = pd.read_pickle('silly_strat_dataframe.pkl')
df_log_returns = np.log(df / df.shift(1))

# a look at efficient frontier of portfolio created on 1 year of daily returns.
# 2015 to 2016 slice

df_hist = df_log_returns.loc['2015':'2016']
mean_returns = df_hist.mean()

ask_to_display('Display historical dataframe?', df_hist)


number_comp = len(df_hist.columns)
weight_guess = number_comp * [1. / number_comp,]

def port_stats(weights):
    weight_array = np.array(weights)
    portfolio_return = np.sum(mean_returns * weight_array)*252
    portfolio_vol = np.sqrt(np.dot(weight_array.T, np.dot(df_hist.cov()* 252, weight_array)))
    sharpe_ratio = portfolio_return / portfolio_vol 
    return np.array([portfolio_return, portfolio_vol, sharpe_ratio])

def max_sharpe(weights):
    return -port_stats(weights)[2]


def min_func_port(weights):
    return port_stats(weights)[1]


cons = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
bnds = tuple((0,1) for x in range(number_comp))

optimize = sciop.minimize(max_sharpe,
                          weight_guess,
                          method = 'SLSQP',
                          bounds= bnds,
                          constraints = cons)


target_returns = np.linspace(-0.10, 0.35, num = 10)
target_volatilites = []
bnds2 = tuple((0,1) for x in range(number_comp))
count2 = 1
for target_return in target_returns:
    cons2 = ({'type': 'eq', 'fun': lambda x, trgt_return = target_return : port_stats(x)[0] - trgt_return},
             {'type': 'eq', 'fun': lambda x: np.sum(x)-1})
    res = sciop.minimize(min_func_port,
                         weight_guess,
                         method = 'SLSQP',
                         bounds = bnds2,
                         constraints = cons2)
    print("Found "+ str(count2) + " target volatilities")
    count2 += 1
    target_volatilites.append(res['fun'])
target_volatilites = np.array(target_volatilites)

plt.figure(figsize = (8,6))
plt.scatter(target_volatilites, target_returns, c = target_returns / target_volatilites, marker = 'o')
plt.plot(port_stats(optimize['x'])[1], port_stats(optimize['x'])[0], 'r*', markersize = 16.0)
#plt.plot(port_stats(optv['x'])[1], stats(optv['x'])[0], 'y*', markersize = 16.0);
plt.grid(True)
plt.colorbar(label = 'Sharpe ratio')

plt.show(block = True)

sys.exit()
