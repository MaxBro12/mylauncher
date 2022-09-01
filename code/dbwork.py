import sqlite3


github_table = '''CREATE TABLE github (
                id INTEGER PRIMARY KEY,
                user TEXT NOT NULL,
                repo TEXT NOT NULL,
                adt TEXT);'''

locdir_table = '''CREATE TABLE local (
                id INTEGER PRIMARY KEY,
                location TEXT NOT NULL)'''


try:
    testsql = sqlite3.connect('test.db')
    testcur = testsql.cursor()
    print(f'База данных {testsql} подключена!')

    testcur.execute(github_table)
    testcur.execute(locdir_table)
    testsql.commit()
    testcur.close()

except sqlite3.Error as error:
    print(f'ОШИБКА: {error}')

finally:
    if testsql:
        testsql.close()
        print('Соединение закрыто!')
