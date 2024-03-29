from os import (
    listdir,
    mkdir,
    remove,
)
from os.path import (
    exists,
    isdir,
)
from requests import get
from shutil import rmtree

from settings import app_files
from gitget import (
    getf
)


def check_empty_folder(check_dir, exept_files=app_files):
    all_files = listdir(check_dir)
    all_files = list(filter(lambda x: x not in exept_files, all_files))
    if len(all_files) > 0:
        return False, all_files
    return True, []


def is_path_correct(local_path: str) -> bool:
    return exists(local_path)


def is_folder(name: str) -> bool:
    return isdir(name)


def create_folder(path: str = 'NewFolder'):
    try:
        mkdir(path)
        return True
    except FileExistsError:
        return False


def remove_file(file_dir: str) -> bool:
    '''Удаляет файл file_name в директории file_dir'''
    try:
        remove(file_dir)
        return True
    except FileNotFoundError:
        return False


def remove_folderAfile(dir_name):
    '''Удаляет все файлы и папки расположенные в dir_name'''
    try:
        rmtree(dir_name)
        return True
    except FileNotFoundError:
        return False


def get_all_files_dirdata():
    pass


# ! =================== С К А Ч И В А Н И Е ===================
def download_repo(files: list, way: str):
    '''Скачивает все файлы и автоматически создает папки'''
    # ! Проверяем существование папки
    if not is_path_correct(way):
        create_folder(way)

    # ! Отделяем названия папок и создаем их
    ways = []
    for f in files:
        w = f['path'].split('/')
        if len(w) > 1:
            w.pop()
            w = '/'.join(w)
            ways.append(w)
    ways = set(ways)
    for w in ways:
        if not exists(f'{way}/{w}'):
            mkdir(f'{way}/{w}')

    # ! Тут скачиваем каждый файл отдельно
    for f in files:
        print(f"Скачивается: {f['name']} Размер: {f['size']}")
        download_file_beta(f, way)


def download_file(f_dict: dict, way: str):
    '''Скачивает файл на путь way'''
    with open(f"{way}/{f_dict['path']}", 'w') as f:
        data = getf(f_dict['url'])
        f.write(data)


def download_file_beta(f_dict: dict, way: str):
    '''Скачивает данные с указаного f_dict в путь way'''
    with get(f_dict['url'], stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(f"{way}/{f_dict['path']}", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def download_file_test(url: str, way: str):
    '''Скачивает данные с указаного url в путь way'''
    local_filename = url.split('/')[-1]
    with get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(f'{way}/{local_filename}', 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename
