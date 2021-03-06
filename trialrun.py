from core.dataloader import pyport_loader
from core.lazysetup import run_i_am_lazy

def mini_run():
    ts_df, instructions = pyport_loader('storageloads/testpickle.pkl', 'testloads/instructions.json')
    ts_df.dropna(axis='columns', how='any', inplace=True)

    allocation, opt_obj = run_i_am_lazy(ts_df)
    return allocation, opt_obj