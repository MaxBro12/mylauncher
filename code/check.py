from os.path import exists
from os import mkdir, getcwd, listdir
from settings import url_set_file, app_files
from requests import get
from dbwork import check_db


def main_check():
    app_dir = getcwd()

    # ! Проверка на наличие лишних файлов в папки с приложением
    empty, files = check_empty_folder(app_dir)
    if not empty:
        print(f'App directory not empty!\nPlease delete or remove files:')
        for i in files:
            print(f'\t{i}')

    # ! Проверки на наличие папки DATA
    check_folder(app_dir)
    check_settings()

    # ! Проверка наличия базы данных
    check_db()


def check_empty_folder(check_dir, exept_files=app_files):
    all_files = listdir(check_dir)
    all_files = list(filter(lambda x: x not in exept_files, all_files))
    if len(all_files) > 0:
        return False, all_files
    return True


def check_folder(wd: str):
    if not exists(f'{wd}/data'):
        mkdir('data')


def check_settings():
    if not exists('data/settings.ini'):
        with open('data/settings.ini', 'w') as set_file:
            set_file.write(get(f'{url_set_file}?raw=true').text)


def download_file(url):
    local_filename = url.split('/')[-1]
    with get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename
