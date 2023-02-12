from os import (
    mkdir,
)
from os.path import (
    exists,
)

from core import (
    get_os,

    # Конфиги
    ConfigException,
    read,
    write,

    # База данных
    create_db,
)

from .settings import (
    data_folder,
    config_file,
    config_dict,
    db_file,
)


def main_check():
    # ? Проверяем файлы
    check_data()

    # ? Подгружаем конфиг
    os = get_os()
    data = read(config_file)
    data['os'] = os
    # match os:
    #     case 'win':
    #         data = win_init()
    #     case 'linux':
    #         data = linux_init()
    #     case 'ios':
    #         print('Приложение не поддерживается на IOS')
    #     case None:
    #         print('Не известная OS')
    #         raise OsException

    # ! Обработка ошибки файла конфига
    if not data:
        raise ConfigException

    return data


def check_data():
    if not exists(data_folder):
        mkdir(data_folder)
    if not exists(config_file):
        write(config_dict, config_file)
    if not exists(db_file):
        create_db(db_file)
