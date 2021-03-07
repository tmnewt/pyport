
from core.settings import BASE_DIR
from core.dataloader import loader
from core.actions import (
    calc_log_returns             , slice_ts_df        , calc_expected_returns_on_slice ,
    calc_covariance_matrix       , optimize_portfolio , set_allocation_bounds ,
    set_optimization_constraints , build_weight_guess
)

def lazy_demo(verbose:bool=False):
    ts_df, instructions = loader(
                        BASE_DIR/'pyport_examples/data/silly.pkl',
                        BASE_DIR/'pyport_examples/instructions/silly.json')
    assets       = list(ts_df.columns.values)
    num_assets   = len(assets)
    lr_df        = calc_log_returns(ts_df)
    lr_slice     = slice_ts_df(lr_df, '2015', '2016')
    mean_returns = calc_expected_returns_on_slice(lr_slice)
    cov_matrix   = calc_covariance_matrix(lr_slice)
    bounds       = set_allocation_bounds(num_assets)
    constraints  = set_optimization_constraints()
    weights      = build_weight_guess(assets)
    allocation, opt_obj = optimize_portfolio(
        weight_arr = weights,
        mean_returns= mean_returns,
        covariance_matrix = cov_matrix,
        constraints=constraints,
        bounds=bounds
    )
    return allocation, opt_obj
