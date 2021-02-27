# February 22nd 2021.

from pathlib import Path
import json

import pandas as pd, numpy as np, scipy.optimize as sciop
import pandas_datareader as pdr
import matplotlib.pyplot as plt

from pandas import DataFrame

def fetch_data(tickers:list, start:str, end:str, interval:str = 'd') -> DataFrame:
    "Will fetch financial data and wrangle it into a pandas dataframe"
    data_pull = pdr.get_data_yahoo(tickers, start, end, interval=interval)
    data_pull = data_pull.loc[:, pd.IndexSlice['Adj Close', :]]
    data_pull.columns = data_pull.columns.levels[1]
    return data_pull


def _pickle_frame(df:DataFrame, output:Path):
    'pickles the dataframe'
    if output.suffix != ".pkl":
        output = output.with_suffix(".pkl")
    df.to_pickle(output)



def get_time_series_dataframe(data_file_path, instructions) -> DataFrame:
    try:
        financial_time_series_dataframe = pd.read_pickle(data_file_path)
    except FileNotFoundError:
        # get data and save it to the name
        print(f'Could not find time series data file "{data_file_path.name}". Downloading and saving')
        financial_time_series_dataframe = fetch_data(**instructions)
        _pickle_frame(financial_time_series_dataframe, data_file_path)
    return financial_time_series_dataframe

def _cast_path_object(pathlike) -> Path:
    if not isinstance(pathlike, Path):
        path_obj = Path(pathlike)
    return path_obj

def raise_error_with_info(error_raised, file_path, extra_notes:str = None):
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    if not file_path.parent.exists():
        notes = f'The parent directory "{file_path.parent}" could not be found.'
    else:
        notes = f'The parent direcotry "{file_path.parent}" was found. Maybe "{file_path.name}" is misspelled?'
    
    message = f"""
    
    The path provided for instruction file "{file_path.name}" does not point to anything!
    
    Details:
    ----------------------
    {notes}
    {extra_notes}"""

    raise error_raised(message)

def _load_instruction(instructions_file:Path) -> dict:
    try:
        with open(instructions_file) as json_file:
            instructions_dict = json.load(json_file)
    except FileNotFoundError:
        raise_error_with_info(FileNotFoundError, instructions_file, "Some form of instructions file is needed. Cannot continue without instructions.")
    return instructions_dict



def pyport_loader(data_file_path:Path, instructions_file:Path) -> DataFrame:
    data_file_path = _cast_path_object(data_file_path)
    instructions_file = _cast_path_object(instructions_file)
    instructions_dict = _load_instruction(instructions_file)
    times_series_dataframe = get_time_series_dataframe(data_file_path, instructions_dict)
    print('Done loading')
    return times_series_dataframe, instructions_dict

def _helper_df_cast(df:DataFrame) -> DataFrame:
    return df

ts_df, instructions = pyport_loader('storageloads/testpickle.pkl', 'testloads/instructions.json')

ts_df = _helper_df_cast(ts_df)

ts_df.dropna(axis='columns', how='any', inplace=True)
log_ts_df = np.log(ts_df / ts_df.shift(1))
log_ts_df = _helper_df_cast(log_ts_df)





#print(log_ts_df)
#print(ts_df.isna().sum())

#print(ts_df.dropna(axis='columns', how='any'))
#print(ts_df.dropna(axis='columns', how='any', thresh=10))
#print(ts_df.dropna(axis='columns', how='all'))

