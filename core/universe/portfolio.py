from numpy import ndarray, dot, array, isnan
from pandas import DataFrame, Timestamp, Series
from scipy.optimize import OptimizeResult

from .attribute_gets import _get_portfolio_timeline_attributes

class Portfolio:

    def __init__(self,
                name:str,
                pyport,
                timeline:dict,
                store_prices_during_lifetime:bool = False
                ):
        self._name = name
        self._pyport = pyport

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
        self._covariance_matrix:        DataFrame
        self._allocation_bounds:        tuple
        self._optimization_constraints: dict
        self._optimization_result:      OptimizeResult
        self._allocation_array:         ndarray
        self._asset_allocation:         list
        self._interval_returns:         ndarray
        self._interval_dates:           ndarray


    def __repr__(self):
        return f"{self.name} of '{self.pyport.name}' universe. Start: {self.start_date} - End: {self.end_date}"

    def __str__(self):
        return f"{self.name} of '{self.pyport.name}' universe. Start: {self.start_date} - End: {self.end_date}"



    @property
    def name(self):
        return self._name

    @property
    def pyport(self):
        return self._pyport

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
                self._prices_during_lifetime = self.pyport.uni_slice_ts_df(self.start_date, self.end_date)
                return self._prices_during_lifetime
        else:
            return self.pyport.uni_slice_ts_df(self.start_date, self.end_date)

    @property
    def log_returns(self) -> DataFrame:
        try:
            return self._log_returns
        except AttributeError:
            self._log_returns = self.pyport.uni_slice_log_ts_df(self.lookback_start, self.lookback_end)
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
        try:
            return self._mean_returns
        except AttributeError:
            self._mean_returns = self.pyport.calc_mean_returns(self.log_returns)
            return self._mean_returns

    @property
    def covariance_matrix(self) -> Series:
        try:
            return self._covariance_matrix
        except AttributeError:
            self._covariance_matrix = self.pyport.calc_log_slice_covariance_matrix(self.log_returns)
            return self._covariance_matrix

    @property
    def allocation_bounds(self):
        try:
            return self._allocation_bounds
        except AttributeError:
            self._allocation_bounds = self.pyport.universal_bounds
            return self._allocation_bounds

    @allocation_bounds.setter
    def allocation_bounds(self, value):
        self._allocation_bounds = value

    @property
    def optimization_constraints(self):
        try:
            return self._optimization_constraints
        except AttributeError:
            self._optimization_constraints = self.pyport.universal_constraints
            return self._optimization_constraints

    @optimization_constraints.setter
    def optimization_constraints(self, value):
        self._optimization_constraints = value


    @property
    def optimization_result(self) -> OptimizeResult:
        try:
            return self._optimization_result
        except AttributeError:
            self._optimization_result = (
                        self.pyport.optimize(
                            self.pyport.guess_weights(len(self.assets)),
                            self.mean_returns,
                            self.covariance_matrix,
                            self.optimization_constraints,
                            self.allocation_bounds))
            return self._optimization_result


    @property
    def allocation_array(self) -> ndarray:
        try:
            return self._allocation_array
        except AttributeError:
            self._allocation_array = self.pyport.get_allocation_array(self.optimization_result)
            return self._allocation_array

    @allocation_array.setter
    def allocation_array(self, value:ndarray):
        self._allocation_array = value


    @property
    def asset_allocation(self) -> list:
        try:
            return self._asset_allocation
        except AttributeError:
            self._asset_allocation = self._humanize_asset_allocation()
            return self._asset_allocation


    def _humanize_asset_allocation(self):
        if len(self.assets) != len(self.allocation_array):
            raise KeyError(f"Unbalanced number of assets ({len(self.assets)}) to number of allocations ({len(self.allocation_array)}). These numbers must match")
        
        return list(zip(self.assets, self.allocation_array))


    # TODO: consider refactoring interval_returns and interval_dates so they are not dependent on each other.
    @property
    def interval_returns(self) -> ndarray:
        try:
            return self._interval_returns
        except AttributeError:
            self._calc_interval_attributes()
            return self._interval_returns

    @property
    def interval_dates(self) -> ndarray:
        try:
            return self._interval_dates
        except AttributeError:
            self._calc_interval_attributes()
            return self._interval_dates


    def _calc_interval_attributes(self) -> ndarray:
        applicable_log_returns_slice = self.pyport.uni_slice_log_ts_df(self.start_date, self.end_date)
        if len(self.allocation_array) != len(applicable_log_returns_slice.columns.values):
            raise KeyError(f'Unbalanced number of assets ({len(self.allocation_array)}) to number of assets in universe ({len(applicable_log_returns_slice.columns.values)}). These numbers must match')
        # TODO: consider checking for asset to asset alignment.
        self._interval_dates = applicable_log_returns_slice.index.values

        return_deltas = []
        for date in self.interval_dates:
            return_deltas.append(dot(applicable_log_returns_slice.loc[date], self.allocation_array))

        return_deltas = array(return_deltas)
        return_deltas[isnan(return_deltas)]=0
        self._interval_returns = return_deltas+1
