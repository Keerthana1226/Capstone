import json

def load_crop_data(path):
    with open(path, 'r') as file:
        return json.load(file)
