from os import (
    listdir,
    mkdir,
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


def is_folder(name: str) -> bool:
    return name.split('.') == 1


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


def download_file(f_dict: dict, way: str):
    '''Скачивает файл на путь way'''
    with open(f"{way}\\{f_dict['path']}", 'w') as f:
        data = get(f_dict['url']).text
        f.write(data)


def download_repo(files: list, way: str):
    '''Скачивает все файлы и автоматически создает папки'''
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
        download_file(f, way)


def download_file_test(url: str, way: str):
    '''Скачивает данные с указаного url в путь way'''
    local_filename = url.split('/')[-1]
    with get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(f'{way}/{local_filename}', 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename
