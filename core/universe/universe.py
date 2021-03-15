from datetime import datetime
from dateutil.relativedelta import relativedelta

from pandas import DataFrame, Timestamp, Series

from ..dataloader import load_universe as dataloader_universe
from ..actions import (
    _calc_log_returns,
    _slice_ts_df,
    _calc_expected_returns_on_slice,
    _calc_covariance_matrix,
    )
from .attribute_gets import (
    _get_universe_attributes,
    _get_command_attributes,
    )
from ..utils import datecalc

# TODO: extract new "rebalance_frequency_strictness" 
class PyPort:
    def __init__(self, port_name:str):
        self._port_name = port_name

        # preserves the initial information. This becomes useful later
        self._initial_universe_instructions, self._ts_df = self._load_initial_universe(self._port_name)
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
        self._assets) = self._get_initial_universe_attributes()

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
        self._long_ceiling,
        self._bounds,
        self._constraints,) = self._get_initial_command_attributes()

        # frequently reused attributes
        self._log_ts_df: DataFrame


        # rolling "temporary" attributes
        self._temp_datatime_start:      str
        self._temp_datatime_end:        str
        self._temp_log_returns_slice:   DataFrame
        self._temp_cov_frame:           DataFrame
        self._lookback_context:         dict
        self._timeline:        list



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


    # Below is the cleanest manner to apply attributes however attributes are runtime dependent. 
    # This can be dangerous and unwieldy. Also creates an issue when linting.
    #def apply_universe_attributes_setattr(self, instructions):
    #    self._apply_universe_attributes_setattr(instructions)
    #def _apply_universe_attributes_setattr(self, instructions):
    #    universe_section = instructions['universe']
    #    for key, value in universe_section.items():
    #        setattr(self, key, value)
    # You could repeat the same process for command attributes, but remember, this is runtime dependent.





    ## PROPERTIES AND SETTERS

    @property
    def name(self):
        return self._port_name

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
        return self._assets

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

    @property
    def can_short(self) -> bool:
        return self._shorting

    @can_short.setter
    def can_short(self, value):
        self._shorting = value

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
    def bounds_command(self) -> str:
        return self._bounds
    
    @property
    def constraints(self) -> str:
        return self._constraints

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

    #@property
    #def temp_log_returns_slice(self):
    #    try:
    #        return self._temp_log_returns_slice
    #    except AttributeError:
    #        self._temp_log_returns_slice = self.log_ts_df[]
#
    #@property
    #def last_cov_frame(self):
    #    try:
    #        return self._recent_cov_frame
    #    except AttributeError:
    #        return
#
    #@property
    #def portfolios(self):
    #    # return list of portfolios built during the universe run
    #    pass

    @property
    def timeline(self):
        try:
            return self._timeline
        except AttributeError:
            self._timeline = self._build_timeline()
            return self._timeline

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



    def run_strategy(self):
        pass







