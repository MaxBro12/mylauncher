from requests import get
from re import match

from .settings import (
    url_ok,

    url_https,
    api_should_be,
)


def status_code(url: str) -> bool:
    """Проверка на статус"""
    if get(url).status_code == url_ok:
        return True
    else:
        return False


def is_url_correct(url: str) -> bool:
    """Проверяет правильность ссылки на гитхаб"""
    if url.startswith(url_https):
        if match(api_should_be, url):
            if status_code(url):
                return True
    return False
