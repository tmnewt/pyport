from pathlib import Path
from core.settings import YOUR_PYPORT_STORAGE

def _try_mkdir(path:Path) -> None:
    try:
        path.mkdir()
    except FileExistsError:
        pass

_try_mkdir(YOUR_PYPORT_STORAGE)

DATA_PATH = YOUR_PYPORT_STORAGE/'data'
_try_mkdir(DATA_PATH)

UNIVERSES_PATH = YOUR_PYPORT_STORAGE/'universes'
_try_mkdir(UNIVERSES_PATH)

#GROUPS_PATH = YOUR_PYPORT_STORAGE/'groups'
#_try_mkdir(GROUPS_PATH)