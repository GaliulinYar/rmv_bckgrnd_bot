from config import BASE_SQLITE
import sqlite3


# def start():
#     """Создание БД sqlite"""
#     conn = sqlite3.connect('base_sqlite_id.sql')
#     cur = conn.cursor()
#
#     cur.execute('''
#            CREATE TABLE IF NOT EXISTS users (
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                id_telegram INTEGER,
#                name TEXT
#            )
#        ''')
#     conn.commit()
#     cur.close()
#     conn.close()


def rec_id_in_base(user_id_telegram, user_name):
    conn = sqlite3.connect(BASE_SQLITE)
    cur = conn.cursor()

    # Проверяем, есть ли пользователь с заданным id_telegram в базе
    cur.execute('SELECT id FROM users WHERE id_telegram = ?', (user_id_telegram,))
    existing_user = cur.fetchone()

    if existing_user:
        # Пользователь уже существует в базе
        print(f"Пользователь с id_telegram={user_id_telegram} уже существует в базе.")
    else:
        # Вставляем нового пользователя в базу данных
        cur.execute('INSERT INTO users (id_telegram, name) VALUES (?, ?)', (user_id_telegram, user_name))
        conn.commit()
        print(f"Добавлен новый пользователь с id_telegram={user_id_telegram} и именем {user_name}.")

    # Закрываем соединение
    cur.close()
    conn.close()


# Функция получения информации о пользователях
def get_users_info():
    conn = sqlite3.connect(BASE_SQLITE)
    cur = conn.cursor()

    # Получаем информацию о пользователях из базы данных
    cur.execute('SELECT id, id_telegram, name FROM users')
    users_info = cur.fetchall()

    # Закрываем соединение
    cur.close()
    conn.close()

    return users_info
