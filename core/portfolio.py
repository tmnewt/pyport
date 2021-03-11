from pathlib import Path
from core.dataloader import load_universe


class Portfolio:

    def __init__(self, portfolio:str):
        self.portfolio = portfolio


    def _load_universe(self, name):
        return load_universe(name)




