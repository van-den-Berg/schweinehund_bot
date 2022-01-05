import json


def read_json(file: str) -> dict:
    file = open(file, 'r')
    json_dict = json.load(file)
    file.close()
    return json_dict


def save_json_overwrite(json_data: dict, file: str):
    file = open(file, 'w')
    json.dump(json_data, file)
    file.close()
