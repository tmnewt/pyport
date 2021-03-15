import numpy
from numpy import ndarray
from pandas import DataFrame, Series, Timestamp
from scipy import optimize
from scipy.optimize import OptimizeResult

from . import defaults


def calc_log_returns(ts_df:DataFrame) -> DataFrame:
    "Returns log returns of time series dataframe"
    return numpy.log(ts_df / ts_df.shift(1))


def slice_ts_df(ts_df:DataFrame, start:Timestamp, end:Timestamp) -> DataFrame:
    """Uses `pandas` `.loc` property to return slice of times series data.\n
    Works for both log-returns and non log-returns time series.\n
    Cannot be used to slice for discreate timeseries..."""
    start   = Timestamp(start)
    end     = Timestamp(end)
    return ts_df.loc[start:end]


def calc_expected_returns_on_slice(ts_df:DataFrame, frequency:int=252) -> Series:
    return ts_df.mean()*frequency


def calc_covariance_matrix(ts_df:DataFrame, frequency:int=252) -> DataFrame:
    return ts_df.cov() * frequency


def calc_correlation_matrix(ts_df:DataFrame) -> DataFrame:
    return ts_df.corr()


def calc_expected_portfolio_return(weight_arr:ndarray, mean_returns:Series) -> float:
    return numpy.sum(mean_returns * weight_arr)


def calc_expected_portfolio_volatility(weight_arr:ndarray, covariance_matrix:DataFrame) -> float:
    return numpy.sqrt(numpy.dot(weight_arr.T, numpy.dot(covariance_matrix, weight_arr)))


def calc_sharpe_ratio(expected_portfolio_return:float, portfolio_volatility:float) -> float:
    return expected_portfolio_return / portfolio_volatility


def portfolio_statics(weights_arr:ndarray, mean_returns:Series, covariance_matrix:DataFrame) -> list:
    portfolio_return = calc_expected_portfolio_return(weights_arr, mean_returns)
    portfolio_volatility = calc_expected_portfolio_volatility(weights_arr, covariance_matrix)
    sharpe_ratio = -1*(portfolio_return / portfolio_volatility)
    return [portfolio_return, portfolio_volatility, sharpe_ratio]



def optimize_portfolio(weight_guess:ndarray,          mean_returns:Series,
                       covariance_matrix:DataFrame, constraints:dict, 
                       bounds):
    optimization_result = optimize.minimize(
        fun = _maximization_helper_sharpe_ratio,
        x0  = weight_guess, 
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

def build_weight_guess(num_assets) -> list:
    return numpy.array(num_assets * [1. / num_assets])


def tracked_returns(period_weights:ndarray, data_frame:DataFrame, df_log_returns:DataFrame) -> ndarray:
    dates = list(data_frame.index.values)
    tracking_returns = []
    for date in dates:
        tracking_returns.append(numpy.dot(df_log_returns.loc[date], period_weights))

    tracking_returns = numpy.array(tracking_returns)
    tracking_returns[numpy.isnan(tracking_returns)]=0
    return tracking_returns + 1


def efficient_frontier(num_assets, mean_returns, covariance_matrix, bounds):
    y_ceiling = max(mean_returns)
    target_frontier_returns = numpy.linspace(0.0, y_ceiling, num=30)
    result_frontier_volatilities= []
    weight_guess = build_weight_guess(num_assets)

    for target in target_frontier_returns:
        cons = ({'type': 'eq', 'fun': lambda x, target = target : calc_expected_portfolio_return(x, mean_returns) - target},
                {'type': 'eq', 'fun': lambda x: numpy.sum(x)-1})
        frontier_volatility = optimize.minimize(
                    fun         = _minimize_volatility,
                    x0          = weight_guess,
                    args        = (covariance_matrix,),
                    bounds      = bounds,
                    constraints = cons)['fun']
        result_frontier_volatilities.append(frontier_volatility)
    result_frontier_volatilities = numpy.array(result_frontier_volatilities)
    return target_frontier_returns, result_frontier_volatilities

def random_portfolio_draws(num_assets:int, mean_returns:ndarray, covariance_matrix:DataFrame,
                                   num_draws:int=1000, track_draw_weights=False):
    if track_draw_weights:
        draw_weights = numpy.zeros(num_draws, num_assets)
    else:
        draw_weights = None
    draw_returns        = numpy.zeros(num_draws)
    draw_volatilities   = numpy.zeros(num_draws)
    draw_sharpe_ratios  = numpy.zeros(num_draws)


    for draw in range(num_draws):
        weights = _generate_random_allocation_weights(num_assets)
        if track_draw_weights:
            draw_weights[draw, :] = weights
        (draw_return, draw_volatility, draw_sharpe_ratio) = portfolio_statics(weights, mean_returns, covariance_matrix)
        draw_returns[draw]       = draw_return
        draw_volatilities[draw]  = draw_volatility
        draw_sharpe_ratios[draw] = draw_sharpe_ratio
    
    return [draw_returns, draw_volatilities, draw_sharpe_ratios, draw_weights]


def _generate_random_allocation_weights(num_assets):
    weights = numpy.array(numpy.random.random(num_assets))
    weights /= numpy.sum(weights)
    return weights

def _minimize_volatility(weights, covariance_matrix):
    return calc_expected_portfolio_volatility(weights, covariance_matrix)


