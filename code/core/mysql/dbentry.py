import sqlite3


def add_to_db(db: sqlite3.Connection, value: dict):
    """Добавляем значение в базу данных"""
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
        return True
    except Exception:
        cursor.close()
        return False


def remove_from_db(db: sqlite3.Connection, repo_name: str) -> list:
    """Удаляем все репозитории с названием repo_name.
    Возвращает список где:
    [0] - bool - успешно ли было произведено удаление
    [1] - список со всей информацией об удалении"""
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
