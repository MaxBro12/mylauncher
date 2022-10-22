from os.path import exists
from os import mkdir, getcwd
from requests import get

from dirwork import check_empty_folder
from settings import url_set_file, version
from requests import get
from dbwork import check_db
from configparser import ConfigParser


def main_check():
    app_dir = getcwd()

    # ! Проверка на наличие лишних файлов в папки с приложением
    empty, files = check_empty_folder(app_dir)
    if not empty:
        print(
            'Внимание! Дериктория приложения занята сторонними файлами\n' +
            'Пожалуйста удалите или переместите данные файлы:'
        )
        for i in files:
            print(f'\t{i}')

    # ! Проверки на наличие папки DATA, TRACKS и SETTINGS
    check_data(app_dir)
    check_tracks(app_dir)
    check_settings()

    # ! Проверка наличия базы данных
    check_db()

    # ! Загрузка конфига
    config = ConfigParser()
    config.read('data/settings.ini')

    # ! Проверка настроек и места положения приложения
    # check_app_dir(app_dir, config)

    # ! Проверка версии приложения
    try:
        config_call = ConfigParser()
        config_call.read_string(get(f'{url_set_file}?raw=true').text)

        if config_call['Main']['version'] != version:
            print(
                'Вы используете старую версию приложения!\n' +
                'Скачайте новую на:\nhttps://github.com/MaxBro12/mylauncher'
            )
    except Exception as error:
        print(
            'Не удалось получить данные о версии приложения!\n' +
            f'{error}'
        )


# ! ======== ПРОВЕРКИ и СОЗДАНИЕ =========
def check_app_dir(app_dir: str, config: ConfigParser):
    if config['Main']['app_patch'] == '':
        pass


def check_data(wd: str):
    if not exists(f'{wd}/data'):
        mkdir('data')


def check_tracks(wd: str):
    if not exists(f'{wd}/tracks'):
        mkdir('tracks')


def check_settings():
    if not exists('data/settings.ini'):
        with open('data/settings.ini', 'w') as set_file:
            set_file.write(get(f'{url_set_file}?raw=true').text)
