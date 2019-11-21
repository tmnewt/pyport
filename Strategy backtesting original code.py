# You can run this entire script as though it were a program.
# The actual project is not intended to be a self-contained program but rather a script.
# ~Tim

print('Loading program...')

import pandas as pd, numpy as np, scipy.optimize as sciop, sys
import pandas_datareader as pdr
import matplotlib.pyplot as plt


def portfolio_optimization(df_log, start, end):
    global df_slice
    df_slice = df_log.loc[start : end]
    global mean_returns
    mean_returns = df_slice.mean()
    number_comp = len(list(df_log.columns.values))
    weight_guess = number_comp * [1. / number_comp,]
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
    bnds = tuple((0,1) for x in range(number_comp)) 
    optimize = sciop.minimize(max_sharpe_ratio,
                          weight_guess,
                          method = 'SLSQP',
                          bounds= bnds,
                          constraints = cons)
    return optimize['x'].round(3)

def portfolio_statistics(weights):
    weight_array = np.array(weights)
    portfolio_return = np.sum(mean_returns * weight_array)*252
    portfolio_vol = np.sqrt(np.dot(weight_array.T, np.dot(df_slice.cov()* 252, weight_array)))
    sharpe_ratio = portfolio_return / portfolio_vol 
    return np.array([portfolio_return, portfolio_vol, sharpe_ratio])

def max_sharpe_ratio(weights):
    return -portfolio_statistics(weights)[2]

def tracked_returns(period_weights, data_frame):
    dates = list(data_frame.index.values)
    tracking_returns = []
    for date in dates:
        tracking_returns.append(np.dot(df_log_returns.loc[date], period_weights))

    tracking_returns = np.array(tracking_returns)
    tracking_returns[np.isnan(tracking_returns)]=0
    return tracking_returns + 1

def forceYesNo():
    '''Asks for input in terms of Yes\\No answer.

    Returns string \'Y\' or \'N\'

    Will continue to ask until answered with \'Y\' or \'N\''''
    
    hold = True
    while hold:
        response = input('Please answer with \'Y\' or \'N\'\n')
        response = response.upper()
        if response in ('Y', 'N'):
            hold = False
    return response

def pause_output():
    output_hold = True
    while output_hold:
        end_hold = input('\nPress return key to continue.\n')
        output_hold = False

print('''\nMessage from Tim Newton:\n
Thanks for exploring this portfolio backtesting and researching program! This python file is its own semi-self-contained program and will exit upon completion.
This version is not intended to be used or updated in the future and will remain as is.
At various points the program will pause and ask for your input, such as right now.''')
pause_output()

print('''\nThe program you are running originated from a python project I built using Jupyter notebook while in graduate school. 
I've lifted it and converted it into this 'executable' program.
You can find the original as part of my PyPortbacktester project on Github:
https://github.com/tmnewt/PyPortbacktester/blob/master/Strategy%20back-testing.ipynb''')
pause_output()

print('''\nMy aim is to demonstrate how python can accellerate researching portfolio strategies. This is just a one off demonstration bundled as a 'program'.
This program itself runs what I dub to be a 'silly' portfolio strategy. The portfolio strategy is purely for demonstration purposeses.
It rebalances every quarter using exactly 2 years of historical data and follows a fixed universe of mid and small cap stocks (and about 9 large cap stocks).
The portfolio start date is January 2017. The oldest observation date is January 2nd 2015. All in all it currently tracks 11 quarters of daily returns.
See the link above for more information on the portfolio strategy and the story behind it.''')
pause_output()

print('''\nFrom start to finish the program will take a couple minutes to complete. 
This program requires the 'silly_strat_dataframe.pkl' file to execute properly. It is a pandas dataframe containing tickers and price data for the portfolio strategy
The 'silly_strat_dataframe.pkl' file can be found in the repo.
If you don't have it, that's ok. This program will ask if you'd like to download a temporary copy of the data.
You will have the option at the end of this program to save the data as silly_strat_dataframe.pkl for future use.''')
pause_output()

# Start of program.

print('\nIs there a copy of the \'silly_strat_dataframe.pkl\' file saved to the same directory as this program?')
answer = forceYesNo()
if answer == 'N':
    print('''\nWould you like to download a temporary copy of this file? If not, the program will exit as it cannot run without the data contained in this file.
The program will retrive the necessary data from Yahoo Finance and build a copy of that file in memory. You will later have the option to save
the copy for the future''')
    sub_answer = forceYesNo()
    if sub_answer == 'Y':
        comp_list = ['LOW','BKNG','DD','AMT','GE','RSG','SNPS','VEEV','CBS','DXC','BG','LAMR','KIM','HELE','SIGI','S','FHB','CRS','AIMC','TEX','FORM','CSGS','AROC','ATRA','ANDE','TELL','GFF','LMNX','ACLS','GOOD','AKBA','RILY','TLRA','LAND','FBMS','NKSH','TWIN']
        print('Downloading the data from yahoo finance.\n')
        df = pdr.get_data_yahoo(comp_list, '2015', '2020', interval = 'd')  # df starts with multindex 
        df = df.loc[:, pd.IndexSlice['Adj Close', :]] # overwrite so each stock only has adjusted close
        df.columns = df.columns.levels[1] # get rid of multindex
        print('Finished downloading temporary file.')
    elif sub_answer == 'N':
        print('This program will now exit')
        sys.exit()
            
if answer == 'Y':
    print('\nLoading dataframe')
    try:
        df = pd.read_pickle('silly_strat_dataframe.pkl')
    except:
        print('''File not found or corrupted. Please check that the name of the file name matches 'silly_strat_dataframe.pkl' and is in the same folder as this program.
        This program will now exit.''')
        sys.exit()


print('Would you like to see the dataframe the program is working with?')
price_data_question = forceYesNo()
if price_data_question == 'Y':
    print(df)
    pause_output()

print('The program will now convert historical prices to log returns.')
df_log_returns = np.log(df / df.shift(1))
print("\nWould you like to see a log return histogram of each stock?")
histogram_answer = forceYesNo()
if histogram_answer == 'Y':
    df_log_returns.hist(bins = 50, figsize = (20,20))
    print("The plot will open in another window. This program will wait until that window is closed")
    plt.show(block = True)
    

print('''\nThe program will now run the silly portfolio strategy. It can take a few minutes to complete.
Once it reaches the 11th quarter (q3-2019) it will be finish.''')

pause_output()

tracked_all_ret = []
wght_q1 = portfolio_optimization(df_log_returns, '2015', '2016') 
track_ret_q1 = tracked_returns(wght_q1, df_log_returns['2017-01':'2017-03'])
tracked_all_ret.append(track_ret_q1)

print('Quarter 1 complete')

wght_q2 = portfolio_optimization(df_log_returns, '2015-03-31', '2017-03-31')
track_ret_q2 = tracked_returns(wght_q2, df_log_returns['2017-04':'2017-06'])
tracked_all_ret.append(track_ret_q2) 

print('Quarter 2 complete')

wght_q3 = portfolio_optimization(df_log_returns, '2015-06-30', '2017-06-30')
track_ret_q3 = tracked_returns(wght_q3, df_log_returns['2017-07':'2017-09'])
tracked_all_ret.append(track_ret_q3)

print('Quarter 3 complete')

wght_q4 = portfolio_optimization(df_log_returns, '2015-09-30', '2017-09-30')
track_ret_q4 = tracked_returns(wght_q4, df_log_returns['2017-10':'2017-12'])
tracked_all_ret.append(track_ret_q4)

print('Quarter 4 complete')

wght_q5 = portfolio_optimization(df_log_returns, '2015-12-31', '2017-12-31')
track_ret_q5 = tracked_returns(wght_q5, df_log_returns['2018-01':'2018-03'])
tracked_all_ret.append(track_ret_q5)

print('Quarter 5 complete')

wght_q6 = portfolio_optimization(df_log_returns, '2016-03-31', '2018-03-31')
track_ret_q6 = tracked_returns(wght_q6, df_log_returns['2018-04':'2018-06'])
tracked_all_ret.append(track_ret_q6)

print('Quarter 6 complete')

wght_q7 = portfolio_optimization(df_log_returns, '2016-06-30', '2018-06-30')
track_ret_q7 = tracked_returns(wght_q7, df_log_returns['2018-07':'2018-09'])
tracked_all_ret.append(track_ret_q7)

print('Quarter 7 complete')

wght_q8 = portfolio_optimization(df_log_returns, '2016-09-30', '2018-09-30')
track_ret_q8 = tracked_returns(wght_q8, df_log_returns['2018-10':'2018-12'])
tracked_all_ret.append(track_ret_q8)

print('Quarter 8 complete')

wght_q9 = portfolio_optimization(df_log_returns, '2016-12-31', '2018-12-31')
track_ret_q9 = tracked_returns(wght_q9, df_log_returns['2019-01':'2019-03'])
tracked_all_ret.append(track_ret_q9)

print('Quarter 9 complete')

wght_q10 = portfolio_optimization(df_log_returns, '2017-03-31', '2019-03-31')
track_ret_q10 = tracked_returns(wght_q10, df_log_returns['2019-04':'2019-06'])
tracked_all_ret.append(track_ret_q10)

print('Quarter 10 complete')

wght_q11 = portfolio_optimization(df_log_returns, '2017-06-30', '2019-06-30')
track_ret_q11 = tracked_returns(wght_q11, df_log_returns['2019-07':'2019-09'])
tracked_all_ret.append(track_ret_q11)

print('Quarter 11 complete')

joined_trading_returns = np.array([1])
for track in tracked_all_ret:
    joined_trading_returns = np.append(joined_trading_returns, track)

print('\nWould you like to see the portfolios performance by itself?')
performance_answer = forceYesNo()
if performance_answer == 'Y':
    print('Plotting portfolio performance. It should appear in another window')
    plt.plot(joined_trading_returns.cumprod())
    print("The plot will open in another window. This program will wait until that window is closed")
    plt.show(block = True)

print('''The program will now plot the portfolio\'s performance against a benchmark. 
For the portfolio strategy the benchmark is the Russell 3000''')

pause_output()

df_rua = pdr.get_data_yahoo('^RUA', '2017', '2020', interval = 'd')
df_rua = df_rua['Adj Close']
df_rua = pd.DataFrame(df_rua)
df_rua_log_returns = np.log(df_rua / df_rua.shift(1))
df_rua_log_returns.fillna(0, inplace = True)
df_rua_log_returns += 1
rua_log_returns = np.array(df_rua_log_returns)

plt.figure(figsize = (8,6))
plt.plot(joined_trading_returns.cumprod(),  label = 'The Portfolio Strategy')
plt.plot(rua_log_returns.cumprod(), label = 'Passive Strategy')
plt.legend(('The Portfolio Strategy', 'Passive Strategy'), loc = 'upper left')
print("The plot will open in another window. This program will wait until that window is closed")
plt.show(block = True)

print('Would you like to save the copy of the data for future use?')
save_answer = forceYesNo()
if save_answer == 'Y':
    df.to_pickle('silly_strat_dataframe.pkl')

print('The program has finished. Thank you for your time.\n')
sys.exit()