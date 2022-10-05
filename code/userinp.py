from types import NoneType
from copy import copy

from gitapi import (
    is_url_correct,
    clean_repo_http,
    get_all_files_data_git,
    get_def_branch_sha
)
from dirwork import (
    is_path_correct,
    check_empty_folder,
    remove_folderAfile,
    download_repo,
)
from dbwork import (
    load_db,
    add_to_db,
    get_all_from_db,
    get_from_db,
    remove_from_db,
    change_data,
)


class UserInp:
    def __init__(self):
        self.progrun = False
        self.commands = {
            'help': self.help,
            'stop': self.stop,
            'track': self.track,
            'list': self.gettracks,
            'downtrack': self.downloadtrack,
            'update': self.updatetracks,
            'getdata': self.gettrack,
            'remove': self.removetrack,
            'checkgit': self.check_git_url,
            'checkpath': self.check_local_dir,
        }
        self.db = load_db()

    def run(self):
        self.progrun = True

        # ! Приветствующий скрипт
        print('Используйте команду "help" для получения помощи')

        while self.progrun:
            self.user_input()

    def user_input(self):
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
                print('Неверная команда!')
                self.user_input()
        else:
            print(f'Неизвестная команда: "{com}"')

    def help(self, adt=None):
        '''Помощь!'''
        if isinstance(adt, NoneType):
            print('Список всех команд:')
            for command in self.commands:
                print(f'\t{command} - {self.commands[command].__doc__}')
        else:
            try:
                adt = str(adt[0])
                if adt in self.commands:
                    print(f'{adt}:\n\t{self.commands[adt].__doc__}')
            except TypeError:
                print(f'Unknown command {adt}, use "help" command')
                self.user_input()

    def stop(self):
        '''Остановка приложения'''
        self.progrun = False

    # ! ================ ОСНОВА ===================
    def check_git_url(self):
        '''Проверяет гитхаб ссылку на её существование'''
        gitlink = str(input('Введите ссылку на репозиторий:\n'))
        if not is_url_correct(gitlink):
            print('URL is not exists!')
            return False
        return gitlink

    def check_local_dir(self):
        '''Проверяет существование данного пути'''
        locallink = str(input('Введите путь к локальной папке:\n'))
        if not is_path_correct(locallink):
            print('Путь до папки не существует!')
            return False
        if not check_empty_folder(locallink)[0]:
            print(
                'В данной папке находятся файлы!' +
                'Рекомендуется их удалить перед установкой'
            )
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
                    f"Название: {i['repo']}\n\tАвтор: {i['user']}",
                    f"\n\tРасположение: {i['local']}"
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

        # ! Вывод
        if ans:
            print(
                f'Название: {ans["repo"]}\n' +
                f'Автор: {ans["user"]}\n' +
                f'Папка: {ans["local"]}\n' +
                f'Ветка: {ans["branch"]}\n' +
                f'Коммит: {ans["sha"]}'
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

    def downloadtrack(self, name: list = None):
        '''Запускает процесс скачивания репозитория.
        Внимание! Репозиторий должен отслеживаться командой track'''
        # ? Если аргумент не передан в функцию
        if name is None:
            name = input('Название репозитория:\n')
        else:
            name = name[0]

        # ? Запрос в бд
        ans = get_from_db(self.db, name)

        # ! Запуск скачивания
        files, ans = get_all_files_data_git(ans)
        download_repo(files, ans['local'])
        change_data(self.db, ans)

    def updatetracks(self):
        '''Запрашивает данные об актуальных версиях репозиториев.
        Так же их скачивает.'''
        try:
            tracks = get_all_from_db(self.db)

            # ? Получаем список репозиториев, требующих обновления
            need_up = []
            for track in tracks:
                new = copy(track)
                new['branch'], new['sha'] = get_def_branch_sha(new)
                if track['sha'] != new['sha']:
                    need_up.append([track, new])

            # ! Сообщаем об обновлении
            print('Данные пакеты требуют обновления:')
            for i in need_up:
                print(
                    f"\tНазвание: {i[0]['repo']}",
                    f"\n\tСтарая версия: {i[0]['sha']}",
                    f"\n\tНовая  версия: {i[1]['sha']}",
                )

            if input('Обновить? [Y / n]') == 'Y':
                for track in need_up:
                    print(track)
                    self.downloadtrack([track[0]['repo']])
        except Exception as error:
            print(error)
