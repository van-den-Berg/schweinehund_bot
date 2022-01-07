import json


def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as read_file:
        json_dict = json.load(read_file)
    return json_dict


def save_json_overwrite(json_data: dict, file_path: str):
    with open(file_path, 'w') as write_file:
        json.dump(json_data, write_file)
