import numpy
from numpy import ndarray
from pandas import DataFrame, Series

from .frametypes import TimeSeriesAssetFrame, LogReturnAssetFrame

def calc_log_returns(ts_df:DataFrame) -> DataFrame:
    "Returns log returns of time series dataframe"
    return numpy.log(ts_df / ts_df.shift(1))


def slice_ts_df(ts_df:DataFrame, start, end) -> DataFrame:
    """Uses `pandas` `.loc` property to return slice of times series data.\n
    Works for both log-returns and non log-returns time series.\n
    Cannot be used to slice for discreate timeseries..."""
    return ts_df.loc[start:end]


def calc_expected_returns_on_slice(ts_df:DataFrame, adjustment:int=252) -> Series:
    return ts_df.mean()*adjustment


def calc_covariance_matrix(ts_df:DataFrame, frequency:int) -> DataFrame:
    return ts_df.cov() * frequency


def calc_correlation_matrix(ts_df:DataFrame) -> DataFrame:
    return ts_df.corr()


def calc_expected_portfolio_return(weight_arr:ndarray, mean_returns:Series) -> float:
    return numpy.sum(mean_returns * weight_arr)


def calc_expected_portfolio_volatility(weight_arr:ndarray, covariance_matrix:DataFrame) -> float:
    return numpy.sqrt(
        numpy.dot(
            weight_arr.T,
            numpy.dot(
                covariance_matrix,
                weight_arr)))


def calc_sharpe_ratio(expected_portfolio_return:float, portfolio_volatility:float) -> float:
    return expected_portfolio_return / portfolio_volatility


def portfolio_statics(weights_arr:ndarray, mean_returns:Series, covariance_matrix:DataFrame) -> list:
    portfolio_return = calc_expected_portfolio_return(weights_arr, mean_returns)
    portfolio_volatility = calc_expected_portfolio_volatility(weights_arr, covariance_matrix)
    sharpe_ratio = portfolio_return / portfolio_volatility
    return [portfolio_return, portfolio_volatility, sharpe_ratio]


def _maximization_helper_sharpe_ratio(weights_arr:ndarray, mean_returns:Series, covariance_matrix:DataFrame) -> float:
    return portfolio_statics(weights_arr, mean_returns, covariance_matrix)[2]


def set_allocation_long_bounds():
    pass


def build_weight_guess(tickers:list) -> list:
    return numpy.array(len(tickers) * [1. / len(tickers)])
