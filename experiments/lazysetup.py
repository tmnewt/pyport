
from core.settings import LAZY_DATASET, LAZY_INSTRUCTIONS
from core.dataloader import loader
from core.actions import (
    calc_log_returns             , slice_ts_df        , calc_expected_returns_on_slice ,
    calc_covariance_matrix       , optimize_portfolio , set_allocation_bounds ,
    set_optimization_constraints , build_weight_guess , portfolio_statics,
    efficient_frontier   , random_portfolio_draws)

from core.visualizations import plot_pyport_basic


def lazy_demo(verbose:bool=False):
    ts_df, instructions = loader(
                        LAZY_DATASET,
                        LAZY_INSTRUCTIONS)
    assets       = list(ts_df.columns.values)
    num_assets   = len(assets)
    lr_df        = calc_log_returns(ts_df)
    lr_slice     = slice_ts_df(lr_df, '2015', '2016')
    mean_returns = calc_expected_returns_on_slice(lr_slice)
    covariance_matrix   = calc_covariance_matrix(lr_slice)
    bounds       = set_allocation_bounds(num_assets)
    constraints  = set_optimization_constraints()
    weight_guess = build_weight_guess(num_assets)
    
    allocation, opt_obj = optimize_portfolio(
        weight_guess = weight_guess,
        mean_returns= mean_returns,
        covariance_matrix = covariance_matrix,
        constraints=constraints,
        bounds=bounds)
    
    solution_info    = portfolio_statics(allocation, mean_returns, covariance_matrix)
    frontier_info    = efficient_frontier(num_assets, mean_returns, covariance_matrix, bounds)
    random_draw_info = random_portfolio_draws(num_assets, mean_returns, covariance_matrix)
    
    plot_pyport_basic(solution_info, frontier_info, random_draw_info)
    #return allocation, opt_obj



def setup_up_to_log_returns():
    ts_df, instructions = loader(
                        LAZY_DATASET,
                        LAZY_INSTRUCTIONS)
    assets       = list(ts_df.columns.values)
    num_assets   = len(assets)
    lr_df        = calc_log_returns(ts_df)

    return locals()