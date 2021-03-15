from pandas import DataFrame, Timestamp, Series
from .attribute_gets import _get_portfolio_timeline_attributes

from .universe import PyPort
class Portfolio:

    def __init__(self, 
                name:str, 
                universe:PyPort, 
                timeline:dict, 
                store_prices_during_lifetime:bool = False
                ):
        self._name = name
        self._universe = universe

        (self._start_date,
        self._end_date,
        self._lookback_start,
        self._lookback_end) = _get_portfolio_timeline_attributes(timeline)

        self._store_prices_during_lifetime = store_prices_during_lifetime

        #self._prior_portfolio: Portfolio
        #self._next_portfolio: Portfolio

        self._prices_during_lifetime:   DataFrame
        self._log_returns:              DataFrame
        self._assets:                   list
        self._mean_returns:             Series


    @property
    def name(self):
        return self._name

    @property
    def universe(self):
        return self._universe

    @property
    def start_date(self) -> Timestamp:
        return self._start_date

    @property
    def end_date(self) -> Timestamp:
        return self._end_date

    @property
    def lookback_start(self) -> Timestamp:
        return self._lookback_start

    @property
    def lookback_end(self) -> Timestamp:
        return self._lookback_end

    @property
    def store_ts_df(self):
        return self._store_prices_during_lifetime
    
    @store_ts_df.setter
    def store_ts_df(self, value):
        self._store_prices_during_lifetime = value



    @property
    def prices_during_lifetime(self) -> DataFrame:
        #Storing the slice here is wasteful
        if self.store_ts_df:
            try:
                return self._prices_during_lifetime
            except AttributeError:
                self._prices_during_lifetime = self.universe.uni_slice_ts_df(self.start_date, self.end_date)
                return self._prices_during_lifetime
        else:
            return self.universe.uni_slice_ts_df(self.start_date, self.end_date)

    @property
    def log_returns(self) -> DataFrame:
        try:
            return self._log_returns
        except AttributeError:
            self._log_returns = self.universe.uni_slice_log_ts_df(self.lookback_start, self.lookback_end)
            return self._log_returns

    @property
    def assets(self) -> list:
        try:
            return self._assets
        except AttributeError:
            self._assets = list(self.log_returns.columns.values)
            return self._assets
    
    @property
    def mean_returns(self) -> Series:
        pass


    