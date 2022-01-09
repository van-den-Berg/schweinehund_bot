import jsonpickle as jsonpickle


def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as read_file:
        json_dict = jsonpickle.decode(read_file.read())
    return json_dict


def save_json_overwrite(json_data, file_path: str):
    with open(file_path, 'w') as write_file:
        write_file.write(jsonpickle.encode(json_data))
