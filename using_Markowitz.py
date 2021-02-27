#### Testing
from markowitz import Markowitz
import pandas as pd, numpy as np

df = pd.read_pickle('silly_strat_dataframe.pkl')
df_log = np.log(df/ df.shift(1))


port = Markowitz(df_log, '2015', '2016', 252)

port.display_portfolio_statistics()

print(port.allocation_by_ticker)

port.display_efficient_frontier(True)


port2 = Markowitz(df_log, '2017', '2017-12-31', 252)
port2.display_portfolio_statistics()
port2.display_efficient_frontier(True)

port3 = Markowitz(df_log, '2018', '2018-12-31', 252)
port3.display_portfolio_statistics()
port3.display_efficient_frontier(True)

port4 = Markowitz(df_log, '2019', '2020', 252)
port4.display_portfolio_statistics()
port4.display_efficient_frontier(True)
