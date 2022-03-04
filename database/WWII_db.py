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
        cur.execute('SELECT COUNT(TEAM) FROM scum_wwii_event ORDER BY TEAM')
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
        cur.execute('SELECT DISCORD_NAME, TEAM FROM scum_wwii_event ORDER BY TEAM')
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
