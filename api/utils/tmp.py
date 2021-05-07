import os
from pathlib import Path


def check_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    return folder_path


PATH = check_folder(Path(os.path.dirname(os.path.realpath(__file__)))\
              / '..' / 'tmp')
