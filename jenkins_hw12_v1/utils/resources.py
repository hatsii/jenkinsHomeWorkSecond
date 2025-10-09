from pathlib import Path

def resource_path(path_file):
    file_path = (Path(__file__).parents[2] / 'resources' / path_file).resolve()
    return str(file_path)