from discord.ext import commands
from discord_components import Button, ButtonStyle
from mysql.connector import Error, MySQLConnection
from database.db_config import read_db_config

db = read_db_config()


def listpacks():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_items order by item_id DESC ')
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


class Bayonet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listpack')
    async def listpack_command(self, ctx, arg: str):
        pack = listpacks()

        for x in pack:
            await ctx.send(x)