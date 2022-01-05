import json


def read_json(file: str) -> dict:
    file = open(file, 'r')
    json_dict = json.load(file)
    file.close()
    return json_dict




