from sys import argv
from core import create_log_file


def main(args: list):
    pass


if __name__ == '__main__':
    try:
        main(argv[1:])
    except Exception as err:
        create_log_file(f'Critical exception found: {err}', 'crit')
