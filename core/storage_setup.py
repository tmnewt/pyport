from core.settings import YOUR_PYPORT_STORAGE

try:
    YOUR_PYPORT_STORAGE.mkdir()
except FileExistsError:
    pass

data_path = YOUR_PYPORT_STORAGE/'data'
try:
    data_path.mkdir()
except FileExistsError:
    pass

instructions = YOUR_PYPORT_STORAGE/'instructions'
try:
    instructions.mkdir()
except FileExistsError:
    pass