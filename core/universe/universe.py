from datetime import datetime
from dateutil.relativedelta import relativedelta

import numpy
from numpy import ndarray
from pandas import DataFrame, Timestamp, Series
from scipy.optimize import OptimizeResult
import matplotlib.pyplot as plt


from ..dataloader import load_universe as dataloader_universe
from ..actions import (
    _calc_log_returns,
    _slice_ts_df,
    _calc_expected_returns_on_slice,
    _calc_covariance_matrix,
    set_allocation_bounds,
    _optimize_result,
    _get_allocation,
    _guess_weights)

from .attribute_gets import (
    _get_universe_attributes,
    _get_command_attributes,)

from ..utils import datecalc
from ..defaults import optimization_constraints
from .portfolio import Portfolio


# TODO: extract new "rebalance_frequency_strictness" 
# TODO: add doc strings
class PyPort:
    def __init__(self, pyport_name:str):
        self._pyport_name = pyport_name

        # preserves the initial information. This becomes useful later
        self._initial_universe_instructions, self._ts_df = self._load_initial_universe(self._pyport_name)
        self._initial_universe_attributes = self._initial_universe_instructions['universe']
        self._initial_command_attributes  = self._initial_universe_instructions['commands']
        self._initial_description         = self._initial_universe_instructions['description']


        # Instance Attributes (known as the universe attributes) which may be altered, but to a lesser extent of command attributes
        # Universe's start and ends dates are typical examples of attributes which may change.
        (self._related_dataset,
        self._analysis_start_date,
        self._analysis_end_date,
        self._interval,
        self._dropna_how,
        self._universe_assets) = self._get_initial_universe_attributes()
        #TODO: fix discrepency between declared assets and actual.

        self._apply_drophow()

        # Instance attributes (known as the command attributes) which are often altered.
        # These are the primary pieces which when changed produce new results
        (self._strategy_start,
        self._lookback_length,
        self._lookback_time_quantifier,
        self._rebalance,
        self._rebalance_frequency,
        self._shorting,
        self._short_limit,
        self._long_floor,
        self._long_ceiling) = self._get_initial_command_attributes()

        # universal attributes
        self._bounds:         tuple
        self._constraints:    dict
        self._log_ts_df:                DataFrame
        self._lookback_context:         dict
        self._timeline:                 list
        self._portfolios:               list
        self._interval_dates:           list
        self._interval_returns:         ndarray
        self._cumulative_returns:       ndarray



    # TODO: add meaningful repr and str support. Perhaps use pandas to get pleasent dataframes
    #def __repr__(self):
    #    for portfolio in self.portfolios:
    #        print(portfolio)
    #def __str__(self):
    #    for portfolio in self.portfolios:
    #        print(portfolio)



    @staticmethod
    def _load_initial_universe(name):
        "Should only run once. Changes to universe are handled elsewhere"
        return dataloader_universe(name)

    def _get_initial_universe_attributes(self):
        "Should only run once. Changes to universe attributes are handled elsewhere"
        return _get_universe_attributes(self._initial_universe_instructions)

    def _get_initial_command_attributes(self):
        "Should only run once. Changes to command attributes are handled elsewhere"
        return _get_command_attributes(self._initial_universe_instructions)

    def _apply_drophow(self):
        self.ts_df.dropna(axis='columns', how=self.dropna_how, inplace=True)



    # TODO: implement method
    #def _check_asset_declared_consistency(self):
    #    """Handles what to do if the assets (the ticker symbols) do not match
    #    the assets listed on the timeseries dataframe.
    #    """
    #    pass





    # TODO: change as many of these properties to follow the lazy evaluation design
    @property
    def name(self):
        return self._pyport_name

    @property
    def initial_universe_instructions(self):
        return self._initial_universe_instructions

    @property
    def ts_df(self) -> DataFrame:
        return self._ts_df

    @property
    def initial_universe_attributes(self):
        return self._initial_universe_attributes

    @property
    def initial_command_attributes(self):
        return self._initial_command_attributes

    @property
    def initial_description(self):
        return self._initial_description

    @property
    def universe_start(self) -> Timestamp:
        return self._analysis_start_date

    @universe_start.setter
    def universe_start(self, value) -> Timestamp:
        self._analysis_start_date = Timestamp(value)

    @property
    def universe_end(self) -> Timestamp:
        return self._analysis_end_date

    @universe_end.setter
    def universe_end(self, value) -> Timestamp:
        self._analysis_end_date = Timestamp(value)

    @property
    def interval(self) -> str:
        return self._interval

    @property
    def dropna_how(self) -> str:
        return self._dropna_how

    @property
    def universe_assets(self) -> list:
        return self._universe_assets

    @property
    def strategy_start(self) -> Timestamp:
        return self._strategy_start

    @strategy_start.setter
    def strategy_start(self, value):
        self._strategy_start = value

    @property
    def strategy_end(self) -> Timestamp:
        return self._analysis_end_date

    @property
    def lookback_length(self) -> int:
        return self._lookback_length

    @lookback_length.setter
    def lookback_length(self, value):
        self._lookback_length = value

    @property
    def lookback_length_quantifier(self) -> str:
        return self._lookback_time_quantifier

    @lookback_length_quantifier.setter
    def lookback_length_quantifier(self, value):
        self._lookback_time_quantifier = value

    @property
    def can_rebalance(self) -> bool:
        return self._rebalance

    @can_rebalance.setter
    def can_rebalance(self, value):
        self._rebalance = value

    @property
    def rebalance_frequency(self) -> str:
        return self._rebalance_frequency

    @rebalance_frequency.setter
    def rebalance_frequency(self, value):
        self._rebalance_frequency = value


    # TODO: resolve how shorting is implemented. Is a negative long position a short? It should be.
    @property
    def can_short(self) -> bool:
        return self._shorting

    @can_short.setter
    def can_short(self, value):
        self._shorting = value

    # TODO: see prior todo
    @property
    def short_limit(self) -> float:
        return self._short_limit

    @short_limit.setter
    def short_limit(self, value):
        self._short_limit = value

    @property
    def long_floor(self) -> float:
        return self._long_floor

    @long_floor.setter
    def long_floor(self, value):
        self._long_floor = value

    @property
    def long_ceiling(self) -> float:
        return self._long_ceiling
    
    @long_ceiling.setter
    def long_ceiling(self, value):
        self._long_ceiling = value

    @property
    def bounds(self) -> str:
        try:
            return self._bounds
        except AttributeError:
            self._bounds = set_allocation_bounds(len(self.universe_assets), self.long_floor, self.long_ceiling)
            return self._bounds

    @bounds.setter
    def bounds(self, value):
        self._bounds = value
    
    @property
    def constraints(self) -> str:
        try:
            return self._constraints
        except AttributeError:
            self._constraints = optimization_constraints
            return self._constraints

    @constraints.setter
    def constraints(self, value):
        self._constraints = value

    @property
    def log_ts_df(self) -> DataFrame:
        try:
            return self._log_ts_df
        except AttributeError:
            # log_ts_df does not exist yet. Build it.
            self._log_ts_df = _calc_log_returns(self.ts_df)
            return self._log_ts_df

    @property
    def lookback_context(self):
        try:
            return self._lookback_context
        except AttributeError:
            self._lookback_context = {self.lookback_length_quantifier: self.lookback_length}
            return self._lookback_context


    @property
    def timeline(self):
        try:
            return self._timeline
        except AttributeError:
            self._timeline = self._build_timeline()
            return self._timeline


    # TODO: this could easily be a function. Consider poping it out of the class.
    def _build_timeline(self) -> dict:
        timelines = {}

        start_date = self.strategy_start
        now = Timestamp(datetime.today())
        count=1
        while start_date < now:
            count_number = f'{count:04}'
            timelines[f'portfolio_{count_number}'] = {}
            timelines[f'portfolio_{count_number}']['start_date'] = start_date

            end_date = datecalc.timeframe_end(start_date, self.rebalance_frequency)
            timelines[f'portfolio_{count_number}']['end_date'] = end_date

            lookback_end = start_date - relativedelta(days=1)
            timelines[f'portfolio_{count_number}']['lookback_start'] = datecalc.lookback(lookback_end, **self.lookback_context)
            timelines[f'portfolio_{count_number}']['lookback_end'] = lookback_end
            
            start_date = end_date + relativedelta(days=1)
            count += 1

        return timelines


    @staticmethod
    def slice_ts_df(ts_df:DataFrame, start:Timestamp, end:Timestamp) -> DataFrame:
        return _slice_ts_df(ts_df, start, end)


    def uni_slice_ts_df(self, start:Timestamp, end:Timestamp) -> DataFrame:
        return self.slice_ts_df(self.ts_df, start, end)


    def uni_slice_log_ts_df(self, start:Timestamp, end:Timestamp) -> DataFrame:
        return self.slice_ts_df(self.log_ts_df, start, end)


    @staticmethod
    def calc_mean_returns(log_return_slice:DataFrame) -> Series:
        return _calc_expected_returns_on_slice(log_return_slice)


    @staticmethod
    def calc_log_slice_covariance_matrix(log_return_slice:DataFrame):
        return _calc_covariance_matrix(log_return_slice)


    @staticmethod
    def optimize(weight_guess:ndarray,          mean_returns:Series,
                covariance_matrix:DataFrame,    constraints:dict, 
                bounds:tuple) -> OptimizeResult:
        result = _optimize_result(weight_guess, mean_returns, covariance_matrix, constraints, bounds)
        return result


    @staticmethod
    def get_allocation_array(result:OptimizeResult) -> ndarray:
        allocation_array = _get_allocation(result)
        return allocation_array


    @staticmethod
    def guess_weights(num_assets:int):
        return _guess_weights(num_assets)

    @property
    def portfolios(self):
        try:
            return self._portfolios
        except AttributeError:
            self._portfolios = self.build_portfolios()
            return self._portfolios

    def build_portfolios(self):
        strategy_portfolios = []
        for portfolio_timeline_name, timeline_dates in self.timeline.items():
            strategy_portfolios.append(Portfolio(portfolio_timeline_name, self, timeline_dates))
        return strategy_portfolios

    @property
    def interval_returns(self):
        try:
            return self._interval_returns
        except AttributeError:
            self._interval_returns = self._calc_interval_returns()
            return self._interval_returns

    def _calc_interval_returns(self):
        interval_returns = numpy.array([1])
        for portfolio in self.portfolios:
            interval_returns = numpy.append(interval_returns, portfolio.interval_returns)
        return interval_returns
    
    
    @property
    def interval_dates(self):
        try:
            return self._interval_dates
        except AttributeError:
            self._interval_dates = self._calc_interval_dates()
            return self._interval_dates


    def _calc_interval_dates(self):
        for i, portfolio in enumerate(self.portfolios):
            if i == 0:
                interval_dates = portfolio.interval_dates
                # need 1 additional date to reach full interval
                day_before = interval_dates[0] - numpy.timedelta64(1, "D")
                interval_dates = numpy.append(day_before, interval_dates)
            else:
                interval_dates = numpy.append(interval_dates, portfolio.interval_dates)
        return interval_dates



    @property
    def cumulative_returns(self) -> Series:
        try:
            return self._cumulative_returns
        except AttributeError:
            #self._cumulative_returns = self.interval_returns.cumprod()
            self._cumulative_returns = Series(self.interval_returns.cumprod(), index=self.interval_dates)
            
            return self._cumulative_returns

    

    def show_cumulative_returns(self):
        plt.figure('cumulative_figure')
        plt.plot(self.cumulative_returns)
        plt.ylabel('Cumulative Returns')
        plt.xlabel('Timeline')
        plt.show(block=True)