
# TODO: clean this up

from pathlib import Path
import json
import pandas
import pandas_datareader as pdr
from pandas import DataFrame

from .storage_setup import DATA_PATH, PYPORTS_PATH
from .universe.namings import KEYWORD

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
    fetch_context['assets'             ] = instructions[KEYWORD.UNIVERSE][KEYWORD.UNIVERSE_ASSETS]
    fetch_context['analysis_start_date'] = instructions[KEYWORD.UNIVERSE][KEYWORD.UNIVERSE_START]
    fetch_context['analysis_end_date'  ] = instructions[KEYWORD.UNIVERSE][KEYWORD.UNIVERSE_END]
    fetch_context['interval'           ] = instructions[KEYWORD.UNIVERSE][KEYWORD.DATA_INTERVAL]
    fetch_context['dropna_how'         ] = instructions[KEYWORD.UNIVERSE][KEYWORD.DROPNA_HOW]
    return fetch_context


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

# Deprecated
def loader(data_file_path:Path, instructions_file:Path, dropna_how:str='any') -> DataFrame:
    data_file_path = _cast_path_object(data_file_path)
    instructions_file = _cast_path_object(instructions_file)
    instructions_dict = _load_instruction(instructions_file)
    times_series_dataframe = get_time_series_dataframe(data_file_path, instructions_dict)
    print('Done loading data and instruction files')
    times_series_dataframe.dropna(axis='columns', how=dropna_how, inplace=True)
    return times_series_dataframe, instructions_dict

def _hint_as_pandas_dataframe(df:DataFrame) -> DataFrame:
    return df


def _save_data(df:DataFrame, path:Path) -> None:
    if path.suffix == "":
        path = path.with_suffix('.pkl')

    if path.suffix == '.pkl':
        df.to_pickle(path)
    elif path.suffix == '.json':
        df.to_json(path)
    elif path.suffix == '.csv':
        df.to_csv(path)
    elif path.suffix == '.xlsx':
        df.to_excel(path)
    else:
        print(f'pyport will not save data to a file with suffix "{path.suffix}". Your data will be dropped at close if you do not explicitly save it yourself.')

def _read_data(path:Path) -> DataFrame:
    if path.suffix == '.pkl':
        data = _hint_as_pandas_dataframe(pandas.read_pickle(path))
    elif path.suffix == '.json':
        data = _hint_as_pandas_dataframe(pandas.read_json(path))
    elif path.suffix == '.csv':
        data = _hint_as_pandas_dataframe(pandas.read_csv(path))
    elif path.suffix == '.xlsx':
        data = _hint_as_pandas_dataframe(pandas.read_excel(path))
    else:
        raise NotImplementedError(f'pyport does not support "{path.suffix}" file types')
    return data


def _load_instructions(path, alt_pyport_location:Path=None):
    alt_pyport_path_found = False 
    path_name=Path(path)
    if path_name.suffix == '.json':
        pass
    else:
        path_name = path_name.with_suffix('.json')

    if alt_pyport_location:
        if not isinstance(alt_pyport_location, Path):
            alt_pyport_location = Path(alt_pyport_location)
        alt_pyport_location = alt_pyport_location/'pyports'
        if not alt_pyport_location.exists():
            raise_error_with_info(FileNotFoundError, alt_pyport_location)
        pyport_location = alt_pyport_location/path_name
        alt_pyport_path_found = True
    else:
        pyport_location = PYPORTS_PATH/path_name

    if not pyport_location.exists():
        if alt_pyport_path_found:
            text = f'Could not find pyport file "{path_name}" at alternative location {alt_pyport_location}'
        else:
            text = f'Could not find pyport file "{path_name}"'
        raise_error_with_info(FileNotFoundError, pyport_location, text)
    instructions = _load_instruction(pyport_location)
    return instructions



def _load_data(dataset_name:str, instructions:dict, alt_pyport_location:Path=None, fetch_missing_data:bool=True, save_dataframe:bool=True):
    if alt_pyport_location:
        if not isinstance(alt_pyport_location, Path):
            alt_pyport_location = Path(alt_pyport_location)
        alt_pyport_location = alt_pyport_location/'data'
        if not alt_pyport_location.exists():
            raise_error_with_info(FileNotFoundError, alt_pyport_location)
        dataset_location = alt_pyport_location/dataset_name
    else:
        dataset_location = DATA_PATH/dataset_name

    if not dataset_location.exists():
        if dataset_location.suffix == "":
            # instructions do not state how data is setup. Provides only a
            # name. Check to see if any existing data files match universe name.
            raise NotImplementedError('Logic for completing load operation without specifying the file type does not exist yet.')

        if fetch_missing_data:
            print('Downloading missing data. This may take a moment...')
            ts_df = fetch_data(**_get_fetch_context(instructions))
            if save_dataframe:
                if dataset_location.suffix == "":
                    print('No file type specified in instructions. Defaulting to ".pkl"')
                    dataset_location = dataset_location.with_suffix('.pkl')
                print(f'preparing to save data at {dataset_location}')
                _save_data(ts_df, dataset_location)
        else:
            raise_error_with_info(FileNotFoundError, dataset_location,
                f'Declared dataset_name "{dataset_name}" cannot be found and you have opted to not fetch any missing data.')
    else:
        ts_df = _read_data(dataset_location)

    return ts_df
