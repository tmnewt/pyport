#from findatapy.util import SwimPool; SwimPool()
#from findatapy.market import Market, MarketDataRequest, MarketDataGenerator
#import pandas as pd, numpy as np, scipy.optimize as sciop, sys
#from datetime import timedelta
#import datetime

#import pandas_datareader as pdr


#pdr.get_data_yahoo()

# class and experiments in the same file...

# when and where should the code handle different observation frequency?
# it would be nice to flip a switch (not literally...) and alter time frames, observation frequencies, etc, for a portfolio.

# thinking that should go somewhere else. 
# but I'd like a feature that catch when the user enters a observation frequence that doesn't make sense given the data.
# ahhh, so many choices to make.

class MarkowitzOptimizer(object):
    def __init__(self, fin_universe_df, obser_start, obser_end , freq_of_obser, btest_start = None, btest_end = None):
        self.fin_universe_df = fin_universe_df
        self.freq_of_obser = freq_of_obser
        self.obser_start = obser_start
        self.obser_end = obser_end
        self.btest_start = btest_start
        self.btest_end = btest_end
        self.has_resutls = False
    



    
    






