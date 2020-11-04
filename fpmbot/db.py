import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('TGBot.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force_user: bool = False, force_table: bool = False, force_admin: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force_user:
        c.execute('DROP TABLE IF EXISTS Users')
    if force_table:
        c.execute('DROP TABLE IF EXISTS Schedule')
    if force_admin:
        c.execute('DROP TABLE IF EXISTS Admins')

    c.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            username    TEXT NOT NULL,
            first_name  TEXT NOT NULL,
            last_name   TEXT NOT NULL,
            kgroup      INTEGER NOT NULL,
            podgroup    INTEGER NOT NULL,
            VK_link     TEXT NOT NULL
        )
    ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS Schedule (
                id          INTEGER PRIMARY KEY,
                group_id    INTEGER NOT NULL,
                group_subid INTEGER NOT NULL,
                deadline    TEXT NOT NULL,
                Num         INTEGER NOT NULL,
                timeline    TEXT NOT NULL,
                audit       TEXT NOT NULL,
                text        TEXT NOT NULL
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS Admins (
                id              INTEGER PRIMARY KEY,
                user_id         INTEGER NOT NULL,
                username        TEXT NOT NULL,
                link            TEXT NOT NULL,
                Perm            TEXT NOT NULL
            )
        ''')

    c.execute('''
               CREATE TABLE IF NOT EXISTS Newsletter (
                   id          INTEGER PRIMARY KEY,
                   user_id     INTEGER NOT NULL,
                   status      BOOLEAN NOT NULL DEFAULT (FALSE)
           )
       ''')
    # Сохранить изменения
    conn.commit()


@ensure_connection
def add_user(conn, user_id: int, username: str, first_name: str, last_name: str, kgroup: int, podgroup: int, vk: str):
    c = conn.cursor()
    c.execute('INSERT INTO Users (user_id, username, first_name, last_name, kgroup, podgroup, VK_link) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (user_id, username, first_name, last_name, kgroup, podgroup, vk))
    conn.commit()

@ensure_connection
def check_reg_user(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"SELECT * FROM Users WHERE user_id='{user_id}'")
    if c.fetchone() is None:
        return False
    else:
        return True

@ensure_connection
def getName(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"SELECT first_name FROM Users WHERE user_id='{user_id}'")
    (res, ) = c.fetchone()
    return res

@ensure_connection
def getSurname(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"SELECT last_name FROM Users WHERE user_id='{user_id}'")
    (res, ) = c.fetchone()
    return res

@ensure_connection
def getKurs_Group(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"SELECT kgroup FROM Users WHERE user_id='{user_id}'")
    (res, ) = c.fetchone()
    return res

@ensure_connection
def getPod_Group(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"SELECT podgroup FROM Users WHERE user_id='{user_id}'")
    (res,) = c.fetchone()
    return res

@ensure_connection
def getVk(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"SELECT VK_link FROM Users WHERE user_id='{user_id}'")
    (res,) = c.fetchone()
    return res


@ensure_connection
def check_adm(conn, user_id: int):
    c = conn.cursor()
    c.execute(f"SELECT * FROM Admins WHERE user_id = '{user_id}'")
    if c.fetchone() is None:
        print(f"Попытка войти в админ панель '{user_id}'")
        return False
    else:
        print(f"Администратор '{user_id}' в сети")
        return True

@ensure_connection
def new_adm_db(conn, user_id: int, username: str, perm: str):
    c = conn.cursor()
    c.execute(
        'INSERT INTO Admins (user_id, username, link, perm) VALUES (?, ?, ?, ?)',
        (user_id, username, getVk(user_id=user_id), perm))
    conn.commit()

@ensure_connection
def add_predmet(conn, user_id: int, pod_group: int, day: str, num: int, predmet: str, audit: str, timeline: str):
    c = conn.cursor()
    c.execute(f"SELECT kgroup FROM Users WHERE user_id='{user_id}'")
    (group, )=c.fetchone()
    c.execute('INSERT INTO Schedule (group_id, group_subid, deadline, Num, timeline, audit, text ) VALUES (?, ?, ?, ?, ?, ?, ?)', (group, pod_group, day, num, timeline, audit, predmet))
    conn.commit()

@ensure_connection
def admin_predmet(conn, group: str, pod_group: int, day: str, num: int, predmet: str, audit: str, timeline:str):
    c = conn.cursor()
    c.execute('INSERT INTO Schedule (group_id, group_subid, deadline, Num, timeline, audit, text ) VALUES (?, ?, ?, ?, ?, ?, ?)', (group, pod_group, day, num, timeline, audit, predmet))
    conn.commit()








@ensure_connection
def getUser(conn):
    c = conn.cursor()
    c.execute('SELECT user_id FROM Newsletter WHERE status = True')
    return c.fetchall()

@ensure_connection
def getPasp(conn, user_id: int, day: str):
    c = conn.cursor()
    c.execute(f"SELECT kgroup FROM Users WHERE user_id='{user_id}'")
    (group, ) = c.fetchone()
    c.execute(f"SELECT podgroup FROM Users WHERE user_id='{user_id}'")
    (podgroup, ) = c.fetchone()
    c.execute(f"SELECT Num, timeline, text, audit FROM Schedule WHERE group_id='{group}' AND group_subid='{podgroup}' AND deadline='{day}'")
    return c.fetchall()

@ensure_connection
def getGroupPasp(conn, group: int, podgroup: int, day: str):
    c = conn.cursor()
    c.execute(f"SELECT Num, timeline, text, audit FROM Schedule WHERE group_id='{group}' AND group_subid='{podgroup}' AND deadline='{day}'")
    return c.fetchall()

@ensure_connection
def changeRasp(conn, user_id: int, pod_group: int, day: str, num: int, audit: str):
    c = conn.cursor()
    c.execute(f"SELECT kgroup FROM Users WHERE user_id='{user_id}'")
    (group, )=c.fetchone()
    c.execute(f"UPDATE Schedule SET audit = '{audit}' WHERE group_id='{group}' AND group_subid='{pod_group}' AND deadline='{day}' AND Num='{num}'")
    conn.commit()

@ensure_connection
def getAllRasp(conn, group: int, pod_group: int, day: str):
    c = conn.cursor()
    c.execute(f"SELECT Num, timeline, text, audit FROM Schedule WHERE group_id='{group}' AND group_subid='{pod_group}' AND deadline='{day}'")
    return c.fetchall()

@ensure_connection
def check_day(conn, user_id: int, pod_group: int, day: str):
    c = conn.cursor()
    c.execute(f"SELECT kgroup FROM Users WHERE user_id='{user_id}'")
    (group,) = c.fetchone()
    c.execute(
        f"SELECT Num, timeline, text, audit FROM Schedule WHERE group_id='{group}' AND group_subid='{pod_group}' AND deadline='{day}'")
    return c.fetchall()


@ensure_connection
def count_messages(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_message WHERE user_id = ? LIMIT 1', (user_id, ))
    (res, ) = c.fetchone()
    return res


@ensure_connection
def list_messages(conn, user_id: int, limit: int = 10):
    c = conn.cursor()
    c.execute('SELECT id, text FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    return c.fetchall()

if __name__=='__main__':
    init_db()
    getUser()