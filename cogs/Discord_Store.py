import random
from datetime import datetime

from discord.ext import commands

from Store.ItemManager import ItemsManager
from Store.ServerStore import ServerStore
from database.Bank_db import coins_update
from database.Shopping_Cart import *
from database.Store_db import *


class DiscordStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_permissions(manage_roles=True)
    async def clear_command(self, ctx, number: int):
        await ctx.reply('delete all message', mention_author=False)
        await ctx.channel.purge(limit=number)

    @commands.command(name='buy')
    async def buy_command(self, ctx, arg: str):
        member = ctx.author
        package = arg
        itemid = get_item_id(package)
        run_channel = self.bot.get_channel(927796274676260944)
        cmd_channel = self.bot.get_channel(925559937323659274)
        code = random.randint(9, 99999)
        order_number = f'#{code}'
        items = item_id()
        btn_ist = str(items)
        count = check_queue()  # Count all for scum_shopping_cart return 0 or 1
        message = None
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        shop_open = "10:00:00"
        if shop_open <= time:
            price = get_price(itemid)
            title = get_title(itemid)
            coins = players_info(member.id)[5]
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            shop_open = "10:00:00"
            if coins < price:
                message = '⚠ : ยอดเงินของคุณไม่เพียงพอสำหรับสั่งซื้อ' \
                          ' ยอดเงินของคุณทั้งหมดคือ ``${:,d}``'.format(coins)
                await ctx.reply(message, mention_author=False)
                return

            elif price <= coins:
                message = f"กรุณารอสักครู่ ระบบกำลังเตรียมจัดส่ง **{title}** ให้คุณ"
                await ctx.reply(message)
                coins_update(member.id, coins - price)
                order = in_order(member.id)  # Count order_number for scum_shopping_cart by discord id return 0 or 1
                add_to_shoping_cart(member.id, member.name, players_info(member.id)[3], order_number, itemid)
                if count == 0:
                    queue = check_queue()
                    checkout = '--run {}'.format(order_number)
                    await cmd_channel.send(
                        f'{member.mention}\n'
                        f'```เลขที่ใบสั่งซื้อ {order_number} อยู่ระหว่างการจัดส่ง'
                        f' จำนวนคิวจัดส่ง {order}/{queue}```')
                    await run_channel.send(checkout)
                    print('run command to send package to player')

                else:
                    queue = check_queue()
                    await cmd_channel.send(
                        f'{member.mention}\n'
                        f'```เลขที่ใบสั่งซื้อ {order_number} อยู่ระหว่างการจัดส่ง'
                        f' จำนวนคิวจัดส่ง {order}/{queue}```', mention_author=False)
                    print('send information without run command')
            return
        elif time <= shop_open:
            message = 'Drone is still unavailable : The shop is open from 10:00 to 24:00.'
            await ctx.reply(message, mention_author=False)
        return False

    @buy_command.error
    async def buy_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument **{}**'.format(error.param), mention_author=False)


def setup(bot):
    bot.add_cog(DiscordStore(bot))
    bot.add_cog(ServerStore(bot))
    bot.add_cog(ItemsManager(bot))
    # bot.add_cog(Bayonet(bot))
