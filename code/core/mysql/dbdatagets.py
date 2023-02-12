import sqlite3


def get_all_from_db(db: sqlite3.Connection):
    """Возвращает список из словарей всех отслеживаемых репозиториев. Ключи:
    'user' - имя пользователя / создателя репозитория
    'repo' - название репозитория
    'adt' - дополнительная ссылка
    'local' - путь к папке, где должен находиться репозиторий
    'branch' - ветка
    'commit' - последний коммит"""
    try:
        cursor = db.cursor()
        cursor.execute(
            """SELECT * FROM tracks"""
        )
        a = cursor.fetchall()
        ans = []
        for i in a:
            b = {
                'user': i[0],
                'repo': i[1],
                'adt': i[2],
                'local': i[3],
                'branch': i[4],
                'commit': i[5],
            }
            ans.append(b)
        cursor.close()
        return ans
    except Exception as error:
        print(error)
        cursor.close()
        return False


def get_from_db(db: sqlite3.Connection, repo_name) -> dict:
    """Возвращает словарь с ключами:
    'user' - имя пользователя / создателя репозитория
    'repo' - название репозитория
    'adt' - дополнительная ссылка
    'local' - путь к папке, где должен находиться репозиторий
    'branch' - ветка
    'commit' - последний коммит"""
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""SELECT * FROM tracks WHERE repo = '{repo_name}'"""
        )
        a = cursor.fetchall()
        ans = {
            'user': a[0][0],
            'repo': a[0][1],
            'adt': a[0][2],
            'local': a[0][3],
            'branch': a[0][4],
            'commit': a[0][5],
        }
        cursor.close()
        return ans
    except Exception as error:
        print(error)
        cursor.close()
        return False
