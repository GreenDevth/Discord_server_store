from database.Players import *


def listitem(item):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_items WHERE commands = %s', (item,))
        row = cur.fetchone()
        while row is not None:
            return row
    except Error as e:
        print(e)


def listpacks(pack):
    """ Run list product to discord channel by listpack commands """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_items where pack = %s order by item_id', (pack,))
        row = cur.fetchall()
        while row is not None:
            return row
        while row is None:
            return False
    except Error as e:
        print(e)


def listcate(cate):
    """ Run list product to discord channel by listcate commands """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_items where cate = %s order by item_id', (cate,))
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


def get_price(itemid):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT price FROM scum_items where item_id = %s', (itemid,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def item_id():
    conn = MySQLConnection(**db)
    cur = conn.cursor()
    cur.execute('SELECT * FROM scum_items')
    rows = [item[0] for item in cur.fetchall()]
    return rows


def get_title(itemid):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT title FROM scum_items where item_id = %s', (itemid,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_item_id(command):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT item_id FROM scum_items WHERE commands = %s', (command,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
