from os.path import (
    exists,
    isdir,
)


def is_path_correct(local_path: str) -> bool:
    return exists(local_path)


def is_folder(name: str) -> bool:
    return isdir(name)
