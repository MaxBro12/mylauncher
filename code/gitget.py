import re
from requests import get


def getf(where: str, raw: bool = True):
    """
    Скачивает файл по ссылке where.
    Необязательный параметр raw (bool) - чисто файл или с гит окружением
    """
    if raw:
        raw = '?raw=true'
    else:
        raw = ''

    try:
        ans = str(get(f'{where}{raw}').text)
        return ans

    except Exception:
        print(f'Ошибка в скачивании файла: {where}')
        return False


def status_code(url: str):
    if get(url).status_code == 200:
        return True
    else:
        return False
