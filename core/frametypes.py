from pandas import DataFrame

class TimeSeriesAssetFrame(DataFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        


class LogReturnAssetFrame(DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

