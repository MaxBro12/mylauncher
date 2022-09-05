from os import (
    listdir,
    remove,
)
from os.path import (
    exists,
)
from requests import get
from shutil import rmtree

from settings import app_files


def check_empty_folder(check_dir, exept_files=app_files):
    all_files = listdir(check_dir)
    all_files = list(filter(lambda x: x not in exept_files, all_files))
    if len(all_files) > 0:
        return False, all_files
    return True, []


def is_path_correct(local_path: str) -> bool:
    return exists(local_path)


def remove_file(file_dir):
    '''Удаляет файл file_name в директории file_dir'''
    remove(f'file_dir')


def remove_folderAfile(dir_name):
    '''Удаляет все файлы и папки расположенные в dir_name'''
    try:
        rmtree(dir_name)
        return True
    except Exception:
        return False


def download_file(url):
    local_filename = url.split('/')[-1]
    with get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename
