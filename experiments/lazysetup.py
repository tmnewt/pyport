
from core.settings import LAZY_DATASET, LAZY_INSTRUCTIONS
from core.dataloader import loader
from core.actions import (
    _calc_log_returns             , _slice_ts_df        , _calc_expected_returns_on_slice ,
    _calc_covariance_matrix       , _optimize_result , set_allocation_bounds ,
    set_optimization_constraints , _guess_weights , portfolio_statics,
    efficient_frontier   , random_portfolio_draws, _get_allocation)

from core.visualizations import show_portfolio_efficient_frontier


def lazy_demo(verbose:bool=False):
    ts_df, instructions = loader(
                        LAZY_DATASET,
                        LAZY_INSTRUCTIONS)
    assets       = list(ts_df.columns.values)
    num_assets   = len(assets)
    lr_df        = _calc_log_returns(ts_df)
    lr_slice     = _slice_ts_df(lr_df, '2015', '2016')
    mean_returns = _calc_expected_returns_on_slice(lr_slice)
    covariance_matrix   = _calc_covariance_matrix(lr_slice)
    bounds       = set_allocation_bounds(num_assets)
    constraints  = set_optimization_constraints()
    weight_guess = _guess_weights(num_assets)
    
    opt_obj = _optimize_result(
        weight_guess = weight_guess,
        mean_returns= mean_returns,
        covariance_matrix = covariance_matrix,
        constraints=constraints,
        bounds=bounds)

    allocation = _get_allocation(opt_obj)
    
    solution_info    = portfolio_statics(allocation, mean_returns, covariance_matrix)
    frontier_info    = efficient_frontier(num_assets, mean_returns, covariance_matrix, bounds)
    random_draw_info = random_portfolio_draws(num_assets, mean_returns, covariance_matrix)
    
    show_portfolio_efficient_frontier(solution_info, frontier_info, random_draw_info)
    #return allocation, opt_obj

