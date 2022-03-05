import discord
import random
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.Store_db import check_queue, add_to_shoping_cart, in_order
from database.Players import players_info


class FishingTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
        fishing_list = ["fishing_gray_set", "fishing_blue_set", "fishing_green_set", "fishing_red_set"]
        run_channel = self.bot.get_channel(927796274676260944)
        cmd_channel = self.bot.get_channel(925559937323659274)
        code = random.randint(9, 99999)
        order_number = f'#{code}'
        count = check_queue()
        queue = check_queue()

        """ Golbal"""
        message = None

        """ Fishing Pack """

        if btn in fishing_list:
            player = players_info(member.id)
            package_name = "dailypack"
            order = in_order(player[2])
            add_to_shoping_cart(member.id, member.name, player[3], order_number, package_name)
            if count == 0:
                message = f"กรุณารอสักครู่ ระบบกำลังเตรียมจัดส่ง เซ็ตอุปกรณ์ตกปลา {btn} ให้คุณ"
                checkout = '--run {}'.format(order_number)
                await run_channel.send(
                    f'{member.mention}\n'
                    f'```เลขที่ใบสั่งซื้อ {order_number} อยู่ระหว่างการจัดส่ง อยู่ในคิวจัดส่ง {order}/{queue}```')
                await run_channel.send(checkout)
            else:
                message = f"กรุณารอสักครู่ ระบบกำลังเตรียมจัดส่ง เซ็ตอุปกรณ์ตกปลา {btn} ให้คุณ"
                await run_channel.send(
                    f'{member.mention}\n'
                    f'```เลขที่ใบสั่งซื้อ {order_number} อยู่ระหว่างการจัดส่ง อยู่ในคิวจัดส่ง {order}/{queue}```')
        await interaction.respond(content=message)

    @commands.command(name='fishing_pack')
    async def fishing_pack(self, ctx):
        await ctx.send(
            file=discord.File('./img/store/fishing_rod.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, label='GRAY SET', custom_id='fishing_gray_set'),
                    Button(style=ButtonStyle.blue, label='BLUE SET', custom_id='fishing_blue_set'),
                    Button(style=ButtonStyle.green, label='GREEN SET', custom_id='fishing_green_set'),
                    Button(style=ButtonStyle.red, label='RED SET', custom_id='fishing_red_set')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(FishingTools(bot))
