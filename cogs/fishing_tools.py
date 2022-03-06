import discord
import random
from datetime import datetime
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.Store_db import check_queue, add_to_shoping_cart, in_order, package_info
from database.Players import players_info
from database.Bank_db import coins_update


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
            package = package_info(btn)
            player = players_info(member.id)
            price = package[3]
            coins = player[5]
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            shop_open = "18:00:00"
            if shop_open <= time:
                if coins < price:
                    message = 'ยอดเงินของคุณไม่เพียงพอสำหรับสั่งซื้อ'
                elif price <= coins:
                    coins_update(member.id, coins - price)
                    order = in_order(player[2])
                    add_to_shoping_cart(member.id, member.name, player[3], order_number, btn)
                    if count == 0:
                        count = check_queue()
                        queue = check_queue()
                        message = f"กรุณารอสักครู่ ระบบกำลังเตรียมจัดส่ง เซ็ตอุปกรณ์ตกปลา ให้คุณ"
                        checkout = '--run {}'.format(order_number)
                        await cmd_channel.send(
                            f'{member.mention}\n'
                            f'```เลขที่ใบสั่งซื้อ {order_number} อยู่ระหว่างการจัดส่ง'
                            f' จำนวนคิวจัดส่ง {order}/{queue}```')
                        await run_channel.send(checkout)
                    else:
                        count = check_queue()
                        queue = check_queue()
                        message = f"กรุณารอสักครู่ ระบบกำลังเตรียมจัดส่ง เซ็ตอุปกรณ์ตกปลา ให้คุณ"
                        await cmd_channel.send(
                            f'{member.mention}\n'
                            f'```เลขที่ใบสั่งซื้อ {order_number} อยู่ระหว่างการจัดส่ง '
                            f'จำนวนคิวจัดส่ง {order}/{queue}```')
            elif time <= shop_open:
                message = 'Drone is still unavailable : the shop has been closed, Shop open is 18:00 - 24:00'
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
