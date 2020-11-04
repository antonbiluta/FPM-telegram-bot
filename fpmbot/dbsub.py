import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('dbsub.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_dbsub(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS subscription')

    c.execute('''CREATE TABLE IF NOT EXISTS subscription (
            id          INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id     VARCHAR(255) NOT NULL,
            status      BOOLEAN NOT NULL DEFAULT (FALSE),
            username    TEXT NOT NULL,
            Team        TEXT NOT NULL
        )
    ''')

    """admins = [(1, 391928208, True, 'antonbiluta', 'Общая'),
              (5, 268084546, False, 'ssosat', 'Общая'),
              (2, 269691634, True, 'AlemaleBa', 'Общая'),
              (3, 722762330, True, 'Анютка', 'Общая'),
              (4, 748050818, True, 'Диана', 'Общая')]

    c.executemany("INSERT INTO subscription VALUES (?,?,?,?,?)", admins)
    conn.commit()"""

    # Сохранить изменения
    conn.commit()


@ensure_connection
def add_subscriber(conn, user_id: int, username: str, team: str):
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM subscription WHERE user_id = '{user_id}'")
    if c.fetchone() is None:
        c.execute('INSERT INTO subscription (user_id, username, Team) VALUES (?, ?, ?)', (user_id, username, team))
        conn.commit()

@ensure_connection
def add_subscriber_all(conn, user_id: int, team: str):
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM subscription WHERE user_id = '{user_id}'")
    if c.fetchone() is None:
        c.execute('INSERT INTO subscription (user_id, username, Team) VALUES (?, ?, ?)', (user_id, user_id, team))
        conn.commit()

@ensure_connection
def check_team(conn, user_id: int, team: str):
    c = conn.cursor()
    c.execute(f"SELECT * FROM subscription WHERE user_id = '{user_id}'")
    if c.fetchone() is None:
        pass
    else:
        c.execute(f"SELECT Team FROM subscription WHERE user_id='{user_id}'")
        if team in c.fetchone():
            print(f"Пользователь '{user_id}' из этой команды '{team}'")
            return True
        else:
            print(f"Пользователь '{user_id}' в другой команде")
            return False

@ensure_connection
def delete_team(conn, user: str):
    c = conn.cursor()
    c.execute(f"DELETE FROM subscription WHERE username='{user}'")
    conn.commit()

@ensure_connection
def delete_user(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"DELETE FROM subscription WHERE user_id='{user_id}'")
    conn.commit()


@ensure_connection
def update_subscription(conn, user_id, team: str):
    """Обновляем статус подписки"""
    c = conn.cursor()
    c.execute(f"UPDATE subscription SET Team = '{team}' WHERE user_id = '{user_id}'")
    conn.commit()


@ensure_connection
def get_subscription(conn, team: str):
    c = conn.cursor()
    c.execute('SELECT user_id FROM subscription WHERE Team = ?', (team,))
    return c.fetchall()

@ensure_connection
def get_subscription_all(conn):
    c = conn.cursor()
    c.execute('SELECT user_id FROM subscription')
    return c.fetchall()

@ensure_connection
def get_adm_list(conn):
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM subscription WHERE status = True")
    return c.fetchall()

@ensure_connection
def check_adm(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"SELECT * FROM subscription WHERE user_id = '{user_id}'")
    if c.fetchone() is None:
        print('Нужно регаться!')
    else:
        c.execute(f"SELECT user_id = '{user_id}' FROM subscription WHERE status = True")
        if c.fetchone() is None:
            print("У пользователя нет прав администратора")
            return False
        else:
            print("Администратор в сети")
            return True

if __name__ == '__main__':
    init_dbsub()
