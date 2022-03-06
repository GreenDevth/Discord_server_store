from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def in_order(discord_id):
    """Count product_code from current discord id"""
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(order_number) FROM scum_shopping_cart_demo WHERE discord_id = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            order = list(row)
            return order[0]
    except Error as e:
        print(e)


def check_queue():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("select count(*) from scum_shopping_cart_demo")
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def add_to_shoping_cart(discord_id, discord_name, steam_id, order_number, package_name):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO scum_shopping_cart_demo(discord_id, discord_name, steam_id, order_number, package_name) "
            "VALUES (%s,%s,%s,%s,%s)",
            (discord_id, discord_name, steam_id, order_number, package_name))
        conn.commit()
        cur.close()
        return False
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def delete_row():
    conn = None
    try:

        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('DELETE FROM scum_shopping_cart_demo LIMIT 1')
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def get_package(pack_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT package_data FROM scum_package WHERE package_name = %s', (pack_name,))
        row = cur.fetchone()
        while row is not None:
            data = list(row)
            return data[0]
    except Error as e:
        print(e)


def get_queue(product_code):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT steam_id, package_name FROM scum_shopping_cart_demo WHERE order_number = %s',
                    (product_code,))
        row = cur.fetchone()
        while row is not None:
            data = list(row)
            return data
    except Error as e:
        print(e)


def package_info(package_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_package WHERE package_name = %s', (package_name,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
    except Error as e:
        print(e)
