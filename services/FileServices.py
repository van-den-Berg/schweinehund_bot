from typing import List

import portalocker
import jsonpickle as jsonpickle

from models import Data


def read_json(file_path: str) -> Data.Data:
    classes_for_decoding = (Data.HabitEntry, Data.GroupUserAccount, Data.Group, Data.User, Data.Data)
    with open(file_path, 'r') as read_file:
        portalocker.lock(read_file, portalocker.LOCK_EX)
        json_obj: Data.Data = jsonpickle.decode(read_file.read(), classes=classes_for_decoding)
        portalocker.unlock(read_file)
    return json_obj


def save_json_overwrite(json_data, file_path: str):
    with open(file_path, 'w') as write_file:
        portalocker.lock(write_file, portalocker.LOCK_EX)
        write_file.write(jsonpickle.encode(json_data))
        portalocker.unlock(write_file)


def read_group_whitelist(file_path: str) -> List[str]:
    with open(file_path) as rf:
        return rf.read().replace(',', '').split()
