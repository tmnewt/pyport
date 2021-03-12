from pandas import DataFrame

from ..dataloader import load_universe as dataloader_universe
from .attribute_gets import (
    _get_universe_attributes,
    _get_command_attributes,
    )

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



    @staticmethod
    def _load_initial_universe(name):
        "Should only be run once. Changes to universe are handled elsewhere"
        return dataloader_universe(name)

    def _get_initial_universe_attributes(self):
        "Should only be run once. Changes to universe attributes are handled elsewhere"
        return _get_universe_attributes(self._initial_universe_instructions)

    def _get_initial_command_attributes(self):
        "Should only be run once. Changes to command attributes are handled elsewhere"
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
    def universe_start(self):
        return self._analysis_start_date

    @universe_start.setter
    def universe_start(self, value):
        self._analysis_start_date = value

    @property
    def universe_end(self):
        return self._analysis_end_date

    @universe_end.setter
    def universe_end(self, value):
        self._analysis_end_date = value

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
    def strategy_start(self):
        return self._strategy_start

    @strategy_start.setter
    def strategy_start(self, value):
        self._strategy_start = value

    @property
    def strategy_end(self):
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
