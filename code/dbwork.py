import sqlite3

from os.path import exists


main_table_c = '''CREATE TABLE tracks (
                user TEXT NOT NULL,
                repo TEXT NOT NULL,
                adt TEXT,
                location TEXT NOT NULL,
                branch TEXT,
                sha TEXT);'''


def check_db():
    if not exists('data/base.db'):
        create_db()


def create_db():
    try:
        sql = sqlite3.connect('data/base.db')
        sqlcursor = sql.cursor()

        sqlcursor.execute(main_table_c)
        sql.commit()
        sqlcursor.close()

    except sqlite3.Error as error:
        print(f'ОШИБКА при создании DB:\n\t{error}')

    finally:
        if sql:
            sql.close()


def load_db() -> sqlite3.Connection:
    return sqlite3.connect('data/base.db')


def add_to_db(db: sqlite3.Connection, value: dict):
    '''Добавляем значение в базу данных'''
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""INSERT INTO tracks (user, repo, adt, location)
            VALUES ('{value['user']}',
            '{value['repo']}',
            '{value['adt']}',
            '{value['location']}');"""
        )
        db.commit()

        cursor.close()
    except Exception:
        cursor.close()
        return False


def change_data(db: sqlite3.Connection, data: dict):
    '''Изменяет значение в базе данных.'''
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""
            UPDATE Tracks SET
            branch =  '{data['branch']}',
            sha = '{data['sha']}'
            WHERE repo = '{data['repo']}'"""
        )

        db.commit()

        cursor.close()
    except Exception:
        cursor.close()
        return False


def get_all_from_db(db: sqlite3.Connection):
    '''Возвращает список из словарей всех отслеживаемых репозиториев. Ключи:
    'user' - имя пользователя / создателя репозитория
    'repo' - название репозитория
    'adt' - дополнительная ссылка
    'local' - путь к папке, где должен находиться репозиторий
    'branch' - ветка
    'sha' - последний коммит'''
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
                'sha': i[5],
            }
            ans.append(b)
        cursor.close()
        return ans
    except Exception as error:
        print(error)
        cursor.close()
        return False


def get_from_db(db: sqlite3.Connection, repo_name) -> dict:
    '''Возвращает словарь с ключами:
    'user' - имя пользователя / создателя репозитория
    'repo' - название репозитория
    'adt' - дополнительная ссылка
    'local' - путь к папке, где должен находиться репозиторий
    'branch' - ветка
    'sha' - последний коммит'''
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
            'sha': a[0][5],
        }
        cursor.close()
        return ans
    except Exception as error:
        print(error)
        cursor.close()
        return False


def remove_from_db(db: sqlite3.Connection, repo_name: str) -> list:
    '''Удаляем все репозитории с названием repo_name.
    Возвращает список где:
    [0] - bool - успешно ли было произведено удаление
    [1] - список со всей информацией об удалении'''
    try:
        cursor = db.cursor()
        cursor.execute(
            f"""DELETE FROM tracks WHERE repo = '{repo_name}'"""
        )
        ans = cursor.fetchall()
        db.commit()
        cursor.close()
        return True, ans
    except Exception as error:
        print(error)
        cursor.close()
        return False, [error]


if __name__ == '__main__':
    # ! Базовый запуск
    check_db()
    db = load_db()
    data = {
        'user': 'MaxBro12',
        'repo': 'mylauncher',
        'adt': None,
        'local': 'here',
        'branch': '',
        'sha': '',
    }

    data_test = get_from_db(db, 'GitApi_test')

    change_data(db, data_test)

    db.close()
