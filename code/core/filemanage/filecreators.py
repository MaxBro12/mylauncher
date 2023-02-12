from os import (
    listdir,
    mkdir,
    remove,
)
from shutil import rmtree


def create_folder(path: str = 'NewFolder'):
    """Создает новую папку"""
    try:
        mkdir(path)
        return True
    except FileExistsError:
        return False


def remove_file(file_name: str) -> bool:
    """Удаляет файл по пути file_name"""
    try:
        remove(file_name)
        return True
    except FileNotFoundError:
        return False


def remove_folderAfile(dir_name: str) -> bool:
    """Удаляет все файлы и папки расположенные в dir_name"""
    try:
        rmtree(dir_name)
        return True
    except FileNotFoundError:
        return False


def check_empty_folder(check_dir: str, exept_files: list) -> list:
    """Проверяет дирректорию check_dir на наличие каких либо файлов,
    игнорируя файлы и папки в списке exept_files.
    Возвращает список где:
    [0] - bool - пустая папка или нет
    [1] - list - список файлов если они есть"""
    all_files = listdir(check_dir)
    all_files = list(filter(lambda x: x not in exept_files, all_files))
    if len(all_files) > 0:
        return False, all_files
    return True, []
