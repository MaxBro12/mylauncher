from types import NoneType

from gitapi import (
    is_url_correct,
    clean_repo_http,
)
from dirwork import (
    is_path_correct,
    check_empty_folder,
    remove_folderAfile,
)
from dbwork import (
    load_db,
    add_to_db,
    get_all_from_db,
    get_from_db,
    remove_from_db,
)


class UserInp:
    def __init__(self):
        self.progrun = False
        self.commands = {
            'help': self.help,
            'stop': self.stop,
            'hello': self.hello,
            'track': self.track,
            'gettracks': self.gettracks,
            'gettrack': self.gettrack,
            'remove': self.removetrack,
        }
        self.db = load_db()

    def run(self):
        self.progrun = True

        while self.progrun:
            self.user_input()

    def user_input(self):  # TODO: Доработать обработку исключений!
        word = str(input(': ')).split()
        com = word[0]
        if com in self.commands:
            command = self.commands[com]
            try:
                if len(word) > 1:
                    addition = word[1::]
                    return command(addition)
                else:
                    return command()
            except TypeError:
                print('Wrong command!')
                self.user_input()
        else:
            print(f'Unknown command: "{com}"')

    def help(self, adt=None):
        if isinstance(adt, NoneType):
            print('List of all commands:')
            for command in self.commands:
                print(f'\t{command} - {self.commands[command].__doc__}')
        else:
            try:
                adt = str(adt[0])
                if adt in self.commands:
                    print(f'info about {adt}:\n\t{self.commands[adt].__doc__}')
            except TypeError:
                print(f'Unknown command {adt}, use "help" command')
                self.user_input()

    def stop(self):
        '''Stopping user input'''
        self.progrun = False

    # * Дополнительные функции или методы
    def hello(self):
        '''Printing hello \\o/'''
        print('Hello, world!')

    def check_git_url(self):
        gitlink = str(input('Введите ссылку на репозиторий:\n'))
        if not is_url_correct(gitlink):
            print('URL is not exists!')
            return False
        return gitlink

    def check_local_dir(self):
        locallink = str(input('Введите путь к локальной папке:\n'))
        if not is_path_correct(locallink):
            print('Путь до папки не существует!')
            return False
        if not check_empty_folder(locallink)[0]:
            print('В данной папке находятся файлы! Рекомендуется их удалить перед установкой')
        return locallink

    def track(self):
        '''Запускает отслеживание GitHub репозитория в локальную папку на компьютере.'''

        # ? Проверяем существование GitHub-репозитория
        gitlink = self.check_git_url()
        if not gitlink:
            return False
        # ? Проверяем существование локальной папки
        locallink = self.check_local_dir()
        if not locallink:
            return False

        # ! Добавляем запрос в бд
        logdata = clean_repo_http(gitlink)
        logdata['location'] = locallink
        add_to_db(self.db, logdata)

    def gettracks(self):
        '''Получить список всех отслеживаний.'''
        ans = get_all_from_db(self.db)
        if len(ans) > 0:
            print('Сейчас отслеживаются эти репозетории:')
            for i in ans:
                print(
                    f'Название: {i[1]}\n\tАвтор: {i[0]}',
                    f'\n\tРасположение: {i[3]}'
                )
        else:
            print('Сейчас нет отслеживаемых репозиториев')

    def gettrack(self, name: list = None):
        '''Получить информацию об определенном репозитории'''
        # ? Если аргумент не передан в функцию
        if name is None:
            name = input('Название репозитория:\n')
        else:
            name = name[0]

        # ? Запрос в бд
        ans = get_from_db(self.db, name)
        if ans:
            print(
                f'Название: {ans[0][1]}\n' +
                f'Автор: {ans[0][0]}\n' +
                f'Папка: {ans[0][3]}\n'
            )
        else:
            print('Такого репозитория нет в базе')
            if input('Попробовать еще раз? Y - Да / n - нет\n') == 'Y':
                self.gettrack()

    def removetrack(self, name: list = None):
        '''Удалить отслеживание определенного репозитория'''
        # ? Если аргумент не передан в функцию
        if name is None:
            name = input('Введите название репозитория:\n')
        else:
            name = name[0]

        # ? Запуск удаления
        if remove_from_db(self.db, name)[0]:
            print(f'{name} отслеживаниe успешно удалено')
        else:
            print('Произошла ошибка при удалении.')

    def downloadtrack(self):
        # TODO: Подключить метод скачивания файлов
        pass
