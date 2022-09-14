from re import match
from requests import get
from typing import Union

from dirwork import download_repo


git_api = 'https://api.github.com/repos'
# dl_1 = 'https://github.com'
# dl_2 = 'blob/master'

dl_1 = 'https://raw.githubusercontent.com/'


def is_url_correct(url: str = '') -> bool:
    '''Проверяет правильность ссылки на гитхаб'''
    api_should_be = r'[https://github.com/]'
    if url.startswith('https:'):
        if match(api_should_be, url):
            if get(url).status_code == 200:
                return True
    return False


def clean_repo_http(url: str = '') -> dict:
    '''Возвращает словарь с ключами:\n
    user - имя пользователя\n
    repo - репозиторий\n
    adt  - дополнительные коренные папки'''
    if is_url_correct(url):
        # ? Очистки
        url = url.replace('https://github.com/', '')
        if url.endswith('.git'):
            url = url.replace('.git', '')
        if url.endswith('#readme'):
            url = url.replace('#readme', '')
        if '//' in url:
            url = url.replace('//', '/')

        # ? Создание словаря
        ans = dict()
        ans['user'], ans['repo'], *ans['adt'] = url.split('/')
        if ans['user'] != '':
            if ans['repo'] != '':
                ans['adt'] = '/'.join(ans['adt'])
                return ans
    return False


def get_api_path(all_files: list) -> list:
    return list(map(lambda x: x['path'], all_files))


def get_def_branch(data: dict) -> str:
    ans = get(f"{git_api}/{data['user']}/{data['repo']}/branches").json()
    return ans[0]['name']


def get_download_link(data: dict, f: list) -> list:
    return f"{dl_1}/{data['user']}/{data['repo']}/{data['branch']}/{f['path']}?raw=true"


def get_content(
    user: str = '',
    repo: str = '',
    adt: str = '',
    api: str = git_api
) -> list:
    '''Получаем список всех файлов в конкретной папке'''
    print(f'{api}/{user}/{repo}/contents/{adt}')
    json = get(f'{api}/{user}/{repo}/contents/{adt}').json()
    return list(map(lambda x: {
        'name': json[x]['name'],
        'path': json[x]['path'],
        'type': json[x]['type'],
        'size': json[x]['size'],
    }, range(len(json))))


def split_folders_files(raw_files: list) -> list:
    files = []
    folders = []

    for raw_file in raw_files:
        if raw_file['type'] == 'file':
            files.append(raw_file)
        elif raw_file['type'] == 'dir':
            folders.append(raw_file)
    return files, folders


def get_all_files_data(url: Union[str, dict], consol: bool = False) -> list:
    # ? Проверка типа
    if type(url) == str:
        data = clean_repo_http(url)
    else:
        data = url

    data['branch'] = get_def_branch(data)

    # ? Базовый запрос файлов
    raw_files = get_content(data['user'], data['repo'], data['adt'])
    files, folders = split_folders_files(raw_files)

    # ? В цикле ищим врутренние папки
    for folder in folders:
        raw_files = get_content(data['user'], data['repo'], folder['name'])
        files_new, folders_new = split_folders_files(raw_files)
        files = files + files_new
        folders = folders + folders_new

    # ? Добавляем в словарь URL
    for f in files:
        f['url'] = get_download_link(data, f)

    # ! Тестовый вывод
    if consol:
        print('Файлы:')
        for f in files:
            print(
                f"\tНазвание: {f['name']}\n" +
                f"\tПуть: {f['path']}\n" +
                f"\tРазмер: {f['size']}\n" +
                f"\tURL: {f['url']}\n"
            )
        print('Папки:')
        for f in folders:
            print(
                f"\tНазвание: {f['name']}\n" +
                f"\tПуть: {f['path']}\n"
            )
    return files


if __name__ == '__main__':
    test_url = r'https://github.com/MaxBro12/GitApi_test'
    test_dict = {
        'user': 'MaxBro12',
        'repo': 'GitApi_test',
        'adt': ''
    }
    # files = get_all_files_data(test_url, True)
    # download_repo(files, r'G:\CODING\_Projects\mylauncher\test')
    # * https://github.com/MaxBro12/mylauncher
