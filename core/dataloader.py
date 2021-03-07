# February 22nd 2021.

from pathlib import Path
import json
import pandas
import pandas_datareader as pdr
from pandas import DataFrame



def fetch_data(assets:list, analysis_start_date:str, analysis_end_date:str,
               interval:str = 'd', dropna_how='any') -> DataFrame:
    "Will fetch financial data and wrangle it into a pandas dataframe"
    data_pull = pdr.get_data_yahoo(assets,
                                   analysis_start_date,
                                   analysis_end_date,
                                   interval=interval)
    data_pull = data_pull.loc[:, pandas.IndexSlice['Adj Close', :]]
    data_pull.columns = data_pull.columns.levels[1]
    data_pull.dropna(axis='columns', how=dropna_how, inplace=True)
    return data_pull


def _pickle_frame(df:DataFrame, output:Path):
    'pickles the dataframe'
    if output.suffix != ".pkl":
        output = output.with_suffix(".pkl")
    df.to_pickle(output)



def get_time_series_dataframe(data_file_path, instructions) -> DataFrame:
    try:
        financial_time_series_dataframe = pandas.read_pickle(data_file_path)
    except FileNotFoundError:
        # get data and save under the title of universe_name
        print(f'Could not find time series data file "{data_file_path.name}". Downloading and saving')
        financial_time_series_dataframe = fetch_data(**_get_fetch_context(instructions))
        _pickle_frame(financial_time_series_dataframe, data_file_path)
    return financial_time_series_dataframe

def _get_fetch_context(instructions:dict) -> dict:
    fetch_context = {}
    fetch_context['assets']              = instructions['universe']['assets']
    fetch_context['analysis_start_date'] = instructions['universe']['analysis_start_date']
    fetch_context['analysis_end_date']   = instructions['universe']['analysis_end_date']
    fetch_context['interval']            = instructions['universe']['interval']
    fetch_context['dropna_how']          = instructions['universe']['dropna_how']
    return fetch_context

def _get_universe_name(instructions:dict) -> str:
    pass

def _cast_path_object(pathlike) -> Path:
    return Path(pathlike)

def _cast_bulk_path_objects(pathlikes:list) -> list:
    return [_cast_path_object(pathlike) for pathlike in pathlikes]

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


def loader(data_file_path:Path, instructions_file:Path, dropna_how:str='any') -> DataFrame:
    data_file_path = _cast_path_object(data_file_path)
    instructions_file = _cast_path_object(instructions_file)
    instructions_dict = _load_instruction(instructions_file)
    times_series_dataframe = get_time_series_dataframe(data_file_path, instructions_dict)
    print('Done loading data and instruction files')
    times_series_dataframe.dropna(axis='columns', how=dropna_how, inplace=True)
    return times_series_dataframe, instructions_dict

def _helper_df_cast(df:DataFrame) -> DataFrame:
    return df
