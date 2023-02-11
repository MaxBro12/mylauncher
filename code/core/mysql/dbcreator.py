import sqlite3

from .exceptions import CreateDbError, LoadDbError


main_table_c = """CREATE TABLE tracks (
                user TEXT NOT NULL,
                repo TEXT NOT NULL,
                adt TEXT,
                location TEXT NOT NULL,
                branch TEXT,
                commit TEXT);"""


def create_db(db_base_name: str):
    """Создает базу данных db_base_name - должно быть с окончанием .db"""
    try:
        sql = sqlite3.connect(db_base_name)
        sqlcursor = sql.cursor()

        sqlcursor.execute(main_table_c)
        sql.commit()
        sqlcursor.close()

    except sqlite3.Error as error:
        raise CreateDbError(error)

    finally:
        if sql:
            sql.close()
            return True
        return False


def load_db(db_name: str) -> sqlite3.Connection:
    """Возвращается база данных под названием db_name.
    Обязательно! Файл должен быть с расширением .db"""
    try:
        return sqlite3.connect(db_name)
    except Exception as err:
        raise LoadDbError(err)
