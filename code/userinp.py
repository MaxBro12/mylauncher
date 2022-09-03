from types import NoneType
from gitapi import is_url_correct
from check import is_path_correct


class UserInp:
    def __init__(self):
        self.progrun = False
        self.commands = {
            'help': self.help,
            'stop': self.stop,
            'hello': self.hello,
            'track': self.track,
        }

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

    # * Твои дополнительные функции или методы
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
        locallink = str(input('Введите ссылку на локальную папку:\n'))
        if not is_path_correct(locallink):
            print('Путь до папки не существует!')
            return False
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
