from os.path import exists
from os import mkdir, getcwd


def main_check():
    app_dir = getcwd()
    check_folder(app_dir)
    check_settings()


def check_folder(wd: str):
    if not exists('data'):
        mkdir('data')


def check_settings():
    if not exists('data/settings.ini'):
        with open('data/settings.ini', 'w') as set_file:
            pass
