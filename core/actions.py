import numpy
from numpy import ndarray
from pandas import DataFrame, Series
from scipy import optimize
from scipy.optimize import OptimizeResult

from . import defaults


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


def calc_covariance_matrix(ts_df:DataFrame, frequency:int=252) -> DataFrame:
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



def optimize_portfolio(weight_arr:ndarray,          mean_returns:Series,
                       covariance_matrix:DataFrame, constraints:dict, 
                       bounds):
    optimization_result = optimize.minimize(
        fun = _maximization_helper_sharpe_ratio,
        x0  = weight_arr, 
        args = (mean_returns, covariance_matrix),
        method = 'SLSQP',
        constraints= constraints,
        bounds = bounds,
        )
    optimization_result = _cast_optimize_result(optimization_result)
    optimized_portfolio_allocation = optimization_result['x'].round(4)
    return optimized_portfolio_allocation, optimization_result

def _cast_optimize_result(result) -> OptimizeResult:
    return result


def _maximization_helper_sharpe_ratio(weights_arr:ndarray, mean_returns:Series, covariance_matrix:DataFrame) -> float:
    return portfolio_statics(weights_arr, mean_returns, covariance_matrix)[2]


def set_allocation_bounds(num_assets, lower_allocation:float=0.0, upper_allocation:float=1.0):
    """Returns allocation bound for assets
    
    To enable shorting of assets set `lower` to be less than 0.\n
    To enable lower floor of asset allocation set `lower`.
    """
    if  lower_allocation > upper_allocation:
        raise ValueError('The lower value must be less than the upper value')
    
    if lower_allocation > (1/num_assets):
        print('Lower value was found to be greater than 1/num_assets! Setting lower value to 0 for safety.')
        lower_allocation = 0.0

    if upper_allocation > 1.0:
        raise ValueError('Upper may not be more than 1.0. This implies borrowing money, something not yet implemented')
    bounds = tuple((lower_allocation, upper_allocation) for _ in range(num_assets))
    return bounds


def set_optimization_constraints(override_constraints_dict:dict=None):
    if override_constraints_dict == None:
        return defaults.optimization_constraints
    return override_constraints_dict

def build_weight_guess(tickers:list) -> list:
    return numpy.array(len(tickers) * [1. / len(tickers)])


def tracked_returns(period_weights:ndarray, data_frame:DataFrame, df_log_returns:DataFrame) -> ndarray:
    dates = list(data_frame.index.values)
    tracking_returns = []
    for date in dates:
        tracking_returns.append(numpy.dot(df_log_returns.loc[date], period_weights))

    tracking_returns = numpy.array(tracking_returns)
    tracking_returns[numpy.isnan(tracking_returns)]=0
    return tracking_returns + 1