from ..dataloader import load_universe as dataloader_universe
from .attribute_gets import (
    _get_universe_attributes,
    _get_command_attributes,
    _get_description
    )

class PyPort:
    def __init__(self, port_name:str):
        self._port_name = port_name

        self._universe_instructions, self._ts_df = self.load_universe(self._port_name)

        (self._related_dataset,
        self._analysis_start_date,
        self._analysis_end_date,
        self._interval,
        self._dropna_how,
        self._assets) = self.get_universe_attributes(self._universe_instructions)

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
        self._constraints,) = self.get_command_attributes(self._universe_instructions)





    ## INITIALIZER HELPERS
    
    def load_universe(self, name):
        return self._load_universe(name)

    @staticmethod
    def _load_universe(name):
        return dataloader_universe(name)

    @staticmethod
    def get_universe_attributes(instructions):
        return _get_universe_attributes(instructions)

    @staticmethod
    def get_command_attributes(instructions):
        return _get_command_attributes(instructions)

    # This is the cleanest manner to apply attributes but this would be done at runtime. This can be dangerous and unwieldy. Also creates an issue when linting.

    #def apply_universe_attributes_setattr(self, instructions):
    #    self._apply_universe_attributes_setattr(instructions)
    #def _apply_universe_attributes_setattr(self, instructions):
    #    universe_section = instructions['universe']
    #    for key, value in universe_section.items():
    #        setattr(self, key, value)




    ## PROPERTIES AND SETTERS

    @property
    def name(self):
        return self._port_name

    @property
    def universe_start(self):
        return self._analysis_start_date

    @universe_start.setter
    def universe_start(self, value):
        self._analysis_start_date = value

    @property
    def universe_end(self):
        return self._analysis_end_date



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

    @property
    def strategy_end(self):
        return self._analysis_end_date

    @property
    def lookback_length(self) -> int:
        return self._lookback_length

    @property
    def lookback_length_quantifier(self) -> str:
        return self._lookback_time_quantifier

    @property
    def can_rebalance(self) -> bool:
        return self._rebalance

    @property
    def rebalance_frequency(self) -> str:
        return self._rebalance_frequency

    @property
    def can_short(self) -> bool:
        return self._rebalance

    @property
    def short_limit(self) -> float:
        return self._short_limit

    @property
    def long_floor(self) -> float:
        return self._long_floor

    @property
    def long_ceiling(self) -> float:
        return self._long_ceiling
    
    @property
    def bounds_command(self) -> str:
        return self._bounds
    
    @property
    def constraints(self) -> str:
        return self._constraints


