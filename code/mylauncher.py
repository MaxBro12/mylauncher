from core import create_log_file
from handlers import (
    main_check,
    Program,
)

from sys import argv


def main(args: list = None):
    config_dict = main_check()
    process = Program(config_dict, args)
    if args is None:
        process.run()


if __name__ == '__main__':
    try:
        argv.pop(0)
        if argv == []:
            argv = None
        main(argv)
    except Exception as er:
        create_log_file(er)
        print(
            'Что-то пошло не так : (\n' +
            'Отправьте файл "error.log" разработчику!\n' +
            'maxbro126@gmail.com'
        )
