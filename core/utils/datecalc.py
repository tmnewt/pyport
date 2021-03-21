from dateutil.relativedelta import relativedelta

import pandas
from pandas import Timestamp

from .allowed_frequencies import MONTH_FREQUENCIES, QUARTER_FREQUENCIES, YEAR_FREQUENCIES

def n_days_from_date(start:Timestamp, n:int):
    end = Timestamp(start) + pandas.offsets.Day(n)
    return end

def quarter_from_date(start:Timestamp):
    end = Timestamp(start) + pandas.offsets.MonthEnd(n=3)
    return end

def strict_quarter_from_date(start):
    end = Timestamp(start) + pandas.offsets.QuarterEnd(startingMonth=3)
    return end


def lookback(end:Timestamp, **kwargs):
    start = end - relativedelta(**kwargs)
    return start


def timeframe_end(start:Timestamp, rebalance_frequency, strictness:str='soft'):
    try:
        rebalance_frequency = int(rebalance_frequency)
    except ValueError:
        pass
    else:
        return n_days_from_date(start, rebalance_frequency)

    if isinstance(rebalance_frequency, str):
        rebalance_frequency = rebalance_frequency.lower()
        if rebalance_frequency in MONTH_FREQUENCIES:
            raise NotImplementedError

        if rebalance_frequency in QUARTER_FREQUENCIES:
            if strictness == 'soft':
                return quarter_from_date(start)
            return strict_quarter_from_date(start)

        if rebalance_frequency in YEAR_FREQUENCIES:
            raise NotImplementedError

    else:
        raise ValueError(f'''"{rebalance_frequency}" is not a recognized rebalance frequency.
        Valid frequencies are any of the following:
        Quarter: {QUARTER_FREQUENCIES}

        or, any number of days expressed as an integer''')

#print('hard_n_days_from_date')
#print(n_days_from_date('2015', 60))
#print(n_days_from_date('2015-01', 60))
#print(n_days_from_date('2015-01-23', 60))
#print(n_days_from_date('2015-02-23', 60))
#print(n_days_from_date('2015-03-23', 60))
#print(n_days_from_date('2015-04-23', 60))
#print(n_days_from_date('2015-08-23', 60))
#print(n_days_from_date('2015-11-23', 60), '\n')
#
#
#print('quarter_from_date')
#print(quarter_from_date('2015'))
#print(quarter_from_date('2015-01'))
#print(quarter_from_date('2015-01-23'))
#print(quarter_from_date('2015-02-23'))
#print(quarter_from_date('2015-03-23'))
#print(quarter_from_date('2015-04-23'))
#print(quarter_from_date('2015-08-23'))
#print(quarter_from_date('2015-11-23'), '\n')
#
#print('strict_quarter_from_date')
#print(strict_quarter_from_date('2015'))
#print(strict_quarter_from_date('2015-01'))
#print(strict_quarter_from_date('2015-01-23'))
#print(strict_quarter_from_date('2015-02-23'))
#print(strict_quarter_from_date('2015-03-23'))
#print(strict_quarter_from_date('2015-04-23'))
#print(strict_quarter_from_date('2015-08-23'))
#print(strict_quarter_from_date('2015-11-23'), '\n')
#
#
#s = Timestamp('2017')
#context = {'years': 2}
#d = lookback(s, **context)
#print(d)
#print(type(d))
