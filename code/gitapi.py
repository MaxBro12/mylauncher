from re import match
from requests import get


git_api = 'https://api.github.com/repos/'


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
        url = url.replace('https://github.com/', '')
        if url.endswith('.git'):
            url = url.replace('.git', '')
        ans = dict()
        ans['user'], ans['repo'], *ans['adt'] = url.split('/')
        return ans
    return False


def get_content(api, user, repo, adt=''):
    '''Получаем список названий всех файлов в папке'''
    json = get(f'{api}/{user}/{repo}/contents/{adt}').json()
    return list(map(lambda x: json[x]['name'], range(len(json))))


def get_folders(list_of_files):
    '''Возвращается только список папок'''
    return list(filter(lambda x: len(x.split('.')) == 1, list_of_files))


def is_folder(file_name: str) -> bool:
    '''Вопрос это папка?'''
    return len(file_name.split('.')) == 1


def get_files(main_api, repos_user, repository, adt_folder='') -> list:
    '''Возвращает список:\n
    [0] - Название папки\n
    [1] - Список файлов в папке'''
    return [adt_folder, get_content(main_api,
                                    repos_user,
                                    repository,
                                    adt_folder)]


def get_all_file_names(mainapi, repos_user, repository, adt_folder='') -> list:
    base_files = get_content(mainapi, repos_user, repository, adt_folder)
    files = []
    for file_name in base_files:
        if not is_folder(file_name):
            print(f'Is file: {file_name}')
            files.append(file_name)
        else:
            print(f'==== Folder: {file_name}')
            files.append(get_files(mainapi, repos_user, repository, file_name))
    return files


if __name__ == '__main__':
    print()

    # * КОНЕЦ
