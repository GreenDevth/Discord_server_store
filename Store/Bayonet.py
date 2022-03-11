from discord.ext import commands
from discord_components import Button, ButtonStyle
from mysql.connector import Error, MySQLConnection
from database.db_config import read_db_config

db = read_db_config()


def listpacks(pack):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_items where pack = %s order by item_id', (pack,))
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


class Bayonet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listpack')
    async def listpack_command(self, ctx, arg: str):
        pack = listpacks(arg)

        for x in pack:
            await ctx.send(
                f'{x[8]}',
                components=[
                    [
                        Button(style=ButtonStyle.green, label=f'BUY THIS ITEM', emoji='🔪', custom_id=f'{x[0]}'),
                        Button(style=ButtonStyle.blue, label='ADD TO CART', emoji='🛒', custom_id=f'{x[2]}'),
                        Button(style=ButtonStyle.red, label='CHECKOUT', emoji='💳', custom_id=f'checkout{x[0]}')
                    ]
                ]
            )

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id

        if btn:
            message = await interaction.respond(content=f'{member.name} is click {btn}')
