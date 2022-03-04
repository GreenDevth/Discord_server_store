from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config
from prettytable import PrettyTable
from tabulate import tabulate

table = PrettyTable()

db = read_db_config()


def wwii_red():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT DISCORD_NAME, TEAM FROM scum_wwii_event WHERE TEAM = 'RED' ")
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


def red_count():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(TEAM) FROM scum_wwii_event WHERE TEAM='RED'")
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def wwii_blue():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT DISCORD_NAME, TEAM FROM scum_wwii_event WHERE TEAM = 'BLUE' ")
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


def blue_count():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(TEAM) FROM scum_wwii_event WHERE TEAM='BLUE'")
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def all_count():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_wwii_event')
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def all_team():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT DISCORD_NAME, TEAM FROM scum_wwii_event')
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


def count_color_team(team):
    if team == 'red_check':
        data = red_count()
        msg = data
        return msg
    elif team == 'blue_check':
        data = blue_count()
        msg = data
        return msg
    elif team == 'all_check':
        data = all_count()
        msg = data
        return msg


def show_players(team):
    head = ["DISCORD NAME", "TEAM"]
    if team == 'red_check':
        data = wwii_red()
        msg = tabulate(data, headers=head, tablefmt="simple")
        return msg.strip()
    elif team == 'blue_check':
        data = wwii_blue()
        msg = tabulate(data, headers=head, tablefmt="simple")
        return msg.strip()
    elif team == 'all_check':
        data = all_team()
        msg = tabulate(data, headers=head, tablefmt="simple")
        return msg.strip()




def players_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
    except Error as e:
        print(e)


def event_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def event_register(discord_name, discord_id, steam_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('INSERT INTO scum_wwii_event(DISCORD_NAME, DISCORD_ID, STEAM_ID) VALUES(%s,%s,%s)',
                    (discord_name, discord_id, steam_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def select_team(discord_id, team):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET TEAM = %s WHERE DISCORD_ID = %s', (team, discord_id,))
        conn.commit()
        cur.execute('SELECT COUNT(TEAM) FROM scum_wwii_event WHERE TEAM = %s', (team,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def teleport_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT TELEPORT FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return False
    except Error as e:
        print(e)


def update_teleport(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET TELEPORT = 0 WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def weapon_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT WEAPON_SET FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return False
    except Error as e:
        print(e)


def uniform_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT UNIFORM_SET FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def update_weapon_status(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET WEAPON_SET = 0 WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def update_uniform_status(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET UNIFORM_SET = 0 WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def team_check(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT TEAM FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def add_to_cart(discord_id, discord_name, steam_id, product_code, package_name):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_shopping_cart(discord_id, discord_name, steam_id, order_number, ' \
              'package_name) VALUES (%s,%s,%s,%s,%s)'
        cur.execute(sql, (discord_id, discord_name, steam_id, product_code, package_name,))
        print('Insert new order name {}'.format(product_code))
        conn.commit()
        cur.close()

    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def check_queue():
    """Count Queue for Shopping Cart"""
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_shopping_cart')
        row = cur.fetchone()
        while row is None:
            queue = 0
            return queue
        while row is not None:
            queue = list(row)
            return queue[0]
    except Error as e:
        print(e)


def in_order(discord_id):
    """Count product_code from current discord id"""
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(order_number) FROM scum_shopping_cart WHERE discord_id = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            order = list(row)
            return order[0]
    except Error as e:
        print(e)
