#### Testing
from experiments import Markowitz
import pandas as pd, numpy as np

df = pd.read_pickle('silly_strat_dataframe.pkl')
df_log = np.log(df/ df.shift(1))


port = Markowitz(df_log, '2015', '2016', 252)

print(port.display_portfolio_statistics())

print(port.allocation_by_ticker)

print(port.display_efficient_frontier(True, True))
