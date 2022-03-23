from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


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


def check_queue():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("select count(*) from scum_shopping_cart")
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def add_to_shoping_cart(discord_id, discord_name, steam_id, order_number, itemid):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO scum_shopping_cart(discord_id, discord_name, steam_id, order_number, item_id) "
            "VALUES (%s,%s,%s,%s,%s)",
            (discord_id, discord_name, steam_id, order_number, itemid))
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
        cur.execute('DELETE FROM scum_shopping_cart LIMIT 1')
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def get_package(itemid):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT package_data FROM scum_package WHERE package_name = %s', (itemid,))
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
        cur.execute('SELECT steam_id, item_id FROM scum_shopping_cart WHERE order_number = %s',
                    (product_code,))
        row = cur.fetchone()
        while row is not None:
            data = list(row)
            return data
    except Error as e:
        print(e)


def package_info(itemid):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_items WHERE item_id = %s', (itemid,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
    except Error as e:
        print(e)


def update_stock(itemid, total):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_items SET in_stock = %s WHERE item_id = %s', (total, itemid,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
        return None
    finally:
        if conn.is_connected():
            conn.close()
            return None


def reset_stock():
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_items SET in_stock = 5 WHERE in_stock = 0')
        conn.commit()
        cur.close()
        return None
    except Error as e:
        print(e)
        return None
    finally:
        if conn.is_connected():
            conn.close()
            return None


def item_level(itemid):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT only_level FROM scum_items WHERE item_id = %s', (itemid,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
        return None


def check_pack(pack_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from scum_items where pack = %s', (pack_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def check_cate(pack_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from scum_items where cate = %s', (pack_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def check_stock(by_pack):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT title, commands, in_stock, price, img FROM scum_items WHERE pack = %s', (by_pack,))
        row = cur.fetchall()
        while row is not None:
            return row
    except Error as e:
        print(e)


def check_stocks(by_cate):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT title, commands, in_stock, price, img FROM scum_items WHERE cate = %s', (by_cate,))
        row = cur.fetchall()
        while row is not None:
            return row
    except Error as e:
        print(e)


def list_cate():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT cate FROM scum_items ORDER BY item_id')
        row = cur.fetchall()
        while row is not None:
            res = list(row)
            return res
    except Error as e:
        print(e)


def list_pack(cate_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT pack FROM scum_items WHERE cate = %s ORDER BY item_id', (cate_name,))
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)



def update_stocks():
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_items SET in_stock=5 WHERE in_stock=0')
        conn.commit()
        print('All product stock is set to 5 items.')
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            msg = "All product stock is set to 5 items."
            return msg.strip()

