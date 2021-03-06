from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta


import numpy
from numpy import ndarray
from pandas import DataFrame, Timestamp, Series
from scipy.optimize import OptimizeResult
import matplotlib.pyplot as plt


from ..dataloader import _load_data, _load_instructions
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
from .namings import KEYWORD


# TODO: fix discrepency between declared assets and universe assets.
# TODO: add doc strings
class PyPort:
    def __init__(self, name:str, alt_pyport_location:Path=None):
        self._name = name
        self._instructions = self.load_pyport_instructions(self.name, alt_pyport_location)

        self._ts_df:                    DataFrame
        self._universe:                 dict
        self._commands:                 dict
        self._description:              str


        # universe category attributes
        self._dataset_name:             str
        self._universe_start:           Timestamp
        self._universe_end:             Timestamp
        self._data_interval:            str
        self._dropna_how:               str
        self._declared_assets:          list

        # command category attributes
        self._strategy_start:           Timestamp
        self._strategy_end:             Timestamp
        self._lookback_length:          int
        self._lookback_quantifier:      str
        self._rebalance:                bool
        self._rebalance_frequency:      str
        self._rebalance_frequency_strictness: str
        self._can_short:                 bool
        self._short_limit:              float
        self._long_floor:               float
        self._long_ceiling:             float

        # derrived attributes
        self._universe_assets:          list
        self._bounds:                   tuple
        self._constraints:              dict
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
    def load_pyport_instructions(name, alt_pyport_location:Path=None):
        return _load_instructions(name, alt_pyport_location)


    @staticmethod
    def load_data(dataset_name:str, instructions:dict, alt_pyport_location:Path=None, fetch_missing_data:bool=True, save_dataframe:bool=True):
        return _load_data(dataset_name, instructions, alt_pyport_location, fetch_missing_data, save_dataframe)

    def _apply_drophow(self):
        self._ts_df.dropna(axis='columns', how=self.dropna_how, inplace=True)


    # TODO: implement method
    def _check_asset_declared_consistency(self):
        """Handles what to do if the assets (the ticker symbols) do not match
        the assets listed on the timeseries dataframe.
        """






    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def instructions(self):
        try:
            return self._instructions
        except AttributeError:
            self._instructions = _load_instructions(self.name)
            return self._instructions

    @property
    def ts_df(self) -> DataFrame:
        try: 
            return self._ts_df
        except AttributeError:
            self._ts_df = _load_data(self.dataset_name, self.instructions)
            self._apply_drophow()
            return self._ts_df

    @property
    def universe(self):
        try:
            return self._universe
        except AttributeError:
            self._universe = self.instructions[KEYWORD.UNIVERSE]
            return self._universe

    @property
    def commands(self):
        try:
            return self._commands
        except AttributeError:
            self._commands = self.instructions[KEYWORD.COMMANDS]
            return self._commands

    @property
    def description(self):
        try:
            return self._description
        except AttributeError:
            self._description = self.instructions[KEYWORD.DESCRIPTION]
            return self._description

    @property
    def dataset_name(self):
        try:
            return self._dataset_name
        except AttributeError:
            self._dataset_name = self.universe[KEYWORD.DATASET_NAME]
            return self._dataset_name

    @dataset_name.setter
    def dataset_name(self, value):
        self._dataset_name = value

    @property
    def universe_start(self) -> Timestamp:
        try:
            return self._universe_start
        except AttributeError:          # TODO: create naming constants module
            self._universe_start = Timestamp(self.universe[KEYWORD.UNIVERSE_START])
            return self._universe_start

    @universe_start.setter
    def universe_start(self, value):
        self._universe_start = Timestamp(value)

    @property
    def universe_end(self) -> Timestamp:
        try:
            return self._universe_end
        except AttributeError:
            self._universe_end = Timestamp(self.universe[KEYWORD.UNIVERSE_END])
            return self._universe_end

    @universe_end.setter
    def universe_end(self, value):
        self._universe_end = Timestamp(value)

    @property
    def data_interval(self) -> str:
        try:
            return self._data_interval
        except AttributeError:
            self._data_interval = self.universe[KEYWORD.DATA_INTERVAL]
            return self._data_interval

    @property
    def dropna_how(self) -> str:
        try:
            return self._dropna_how
        except AttributeError:
            self._dropna_how = self.universe[KEYWORD.DROPNA_HOW]
            return self._dropna_how


    @property
    def universe_assets(self):
        try:
            return self._universe_assets
        except AttributeError:
            self._universe_assets = self._update_universe_assets()
            return self._universe_assets

    def _update_universe_assets(self):
        return self.ts_df.columns.values

    # TODO fix declared_assets to not rely on universe assets keyword
    @property
    def declared_assets(self) -> list:
        try:
            return self._declared_assets
        except AttributeError:
            self._declared_assets = self.universe[KEYWORD.UNIVERSE_ASSETS]
            return self._declared_assets
    # TODO re-implement declared_assets.setter when safe
    #@declared_assets.setter
    #def declared_assets(self, value):
    #    self._declared_assets = value

    @property
    def strategy_start(self) -> Timestamp:
        try:
            return self._strategy_start
        except AttributeError:
            self._strategy_start = Timestamp(self.commands[KEYWORD.STRATEGY_START])
            return self._strategy_start

    @strategy_start.setter
    def strategy_start(self, value):
        self._strategy_start = Timestamp(value)

    @property
    def strategy_end(self) -> Timestamp:
        try:
            return self._strategy_end
        except AttributeError:
            try:
                self._strategy_end = self.commands[KEYWORD.STRATEGY_END]
            except KeyError:
                self._strategy_end = self.universe_end
            return self._strategy_end

    @strategy_end.setter
    def strategy_end(self, value):
        self._universe_end = Timestamp(value)

    @property
    def lookback_length(self) -> int:
        try:
            return self._lookback_length
        except AttributeError:
            self._lookback_length = int(self.commands[KEYWORD.LOOKBACK_LENGTH])
            return self._lookback_length

    @lookback_length.setter
    def lookback_length(self, value):
        self._lookback_length = value

    @property
    def lookback_quantifier(self) -> str:
        try:
            return self._lookback_quantifier
        except AttributeError:
            self._lookback_quantifier = self.commands[KEYWORD.LOOKBACK_QUANTIFIER]
            return self._lookback_quantifier

    @lookback_quantifier.setter
    def lookback_quantifier(self, value):
        self._lookback_quantifier = value

    @property
    def can_rebalance(self) -> bool:
        try:
            return self._rebalance
        except AttributeError:
            self._rebalance = self.commands[KEYWORD.CAN_REBALANCE]
            return self._rebalance

    @can_rebalance.setter
    def can_rebalance(self, value):
        if not isinstance(value, bool):
            raise TypeError(f'value "{value}" is not a boolean.')
        self._rebalance = value

    @property
    def rebalance_frequency(self) -> str:
        try:
            return self._rebalance_frequency
        except AttributeError:
            self._rebalance_frequency = self.commands[KEYWORD.REBALANCE_FREQUENCY]
            return self._rebalance_frequency

    @rebalance_frequency.setter
    def rebalance_frequency(self, value):
        self._rebalance_frequency = value


    @property
    def rebalance_frequency_strictness(self):
        try:
            return self._rebalance_frequency_strictness
        except AttributeError:
            try:
                self._rebalance_frequency_strictness = self.commands[KEYWORD.REBALANCE_FREQUENCY_STRICTNESS]
            except KeyError:
                self._rebalance_frequency_strictness = 'soft'
        return self._rebalance_frequency_strictness

    @rebalance_frequency_strictness.setter
    def rebalance_frequency_strictness(self, value):
        self._rebalance_frequency_strictness = value


    # TODO: resolve how shorting is implemented. Is a negative long position a short? It should be.
    @property
    def can_short(self) -> bool:
        try:
            return self._can_short
        except AttributeError:
            self._can_short = self.commands[KEYWORD.CAN_SHORT]
            return self._can_short

    @can_short.setter
    def can_short(self, value):
        if not isinstance(value, bool):
            raise TypeError(f'value "{value}" is not a boolean.')
        self._can_short = value

    # TODO: see prior todo
    @property
    def short_limit(self) -> float:
        try:
            return self._short_limit
        except AttributeError:
            self._short_limit = self.commands[KEYWORD.SHORT_LIMIT]
            return self._short_limit

    @short_limit.setter
    def short_limit(self, value):
        self._short_limit = value

    @property
    def long_floor(self) -> float:
        try:
            return self._long_floor
        except AttributeError:
            self._long_floor = self.commands[KEYWORD.LONG_FLOOR]
            return self._long_floor

    @long_floor.setter
    def long_floor(self, value):
        self._long_floor = value

    @property
    def long_ceiling(self) -> float:
        try:
            return self._long_ceiling
        except AttributeError:
            self._long_ceiling = self.commands[KEYWORD.LONG_CEILING]
            return self._long_ceiling

    @long_ceiling.setter
    def long_ceiling(self, value):
        self._long_ceiling = value

    @property
    def bounds(self) -> str:
        try:
            return self._bounds
        except AttributeError:
            self._bounds = set_allocation_bounds(len(self.declared_assets), self.long_floor, self.long_ceiling)
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
            self._lookback_context = {self.lookback_quantifier: self.lookback_length}
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