import random
from datetime import datetime

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from database.Bank_db import coins_update
from database.Players import players_info
from database.Shopping_Cart import listpacks, get_price, item_id, get_title, listitem
from database.Store_db import in_order, check_queue, add_to_shoping_cart


class Bayonet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listitem')
    async def listitem_command(self, ctx, arg: str):
        x = listitem(arg)
        embed = discord.Embed(
            title='{}'.format(x[1])
        )
        embed.set_image(url=x[8])
        embed.add_field(name='VALUE', value='${:,d}'.format(x[5]))
        embed.add_field(name='COMMAND', value='$buy {}'.format(x[2]))
        embed.add_field(name='COMMAND CHANNEL', value='<#925559937323659274>')
        embed.add_field(name='DESCRIPTION', value='{}'.format(x[3]), inline=False)
        await ctx.send(
            embed=embed,
            components=[
                [
                    Button(style=ButtonStyle.green, label=f'BUY NOW', emoji='💵', custom_id=f'{x[0]}'),
                    Button(style=ButtonStyle.blue, label='ADD TO CART', emoji='🛒', custom_id='add_to_cart'),
                    Button(style=ButtonStyle.red, label='CHECKOUT', emoji='💳', custom_id='checkout')
                ]
            ]
        )

    @listitem_command.error
    async def listitem_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('You can not use this command', mention_author=False)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Mission required argument : {}'.format(error.param))

    @commands.command(name='listpack')
    @commands.has_permissions(manage_roles=True)
    async def listpack_command(self, ctx, arg: str):
        pack = listpacks(arg)
        for x in pack:
            embed = discord.Embed(
                title='{}'.format(x[1])
            )
            embed.set_image(url=x[8])
            embed.add_field(name='VALUE', value='${:,d}'.format(x[5]))
            embed.add_field(name='COMMAND', value='$buy {}'.format(x[2]))
            embed.add_field(name='COMMAND CHANNEL', value='<#925559937323659274>')
            embed.add_field(name='DESCRIPTION', value='{}'.format(x[3]), inline=False)
            await ctx.send(
                embed=embed,
                components=[
                    [
                        Button(style=ButtonStyle.green, label=f'BUY NOW', emoji='💵', custom_id=f'{x[0]}'),
                        Button(style=ButtonStyle.blue, label='ADD TO CART', emoji='🛒', custom_id='add_to_cart'),
                        Button(style=ButtonStyle.red, label='CHECKOUT', emoji='💳', custom_id='checkout')
                    ]
                ]
            )

    @listpack_command.error
    async def listpack_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('You can not use this command', mention_author=False)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Mission required argument : {}'.format(error.param))

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
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
            if btn in btn_ist:
                print(btn)
                price = get_price(btn)
                print(price)
                title = get_title(btn)
                coins = players_info(member.id)[5]
                now = datetime.now()
                time = now.strftime("%H:%M:%S")
                shop_open = "10:00:00"
                if coins < price:
                    message = '⚠ : ยอดเงินของคุณไม่เพียงพอสำหรับสั่งซื้อ' \
                              ' ยอดเงินของคุณทั้งหมดคือ ``${:,d}``'.format(coins)
                    await interaction.respond(content=message)
                    return

                elif price <= coins:
                    message = f"กรุณารอสักครู่ ระบบกำลังเตรียมจัดส่ง **{title}** ให้คุณ"
                    await interaction.respond(content=message)
                    coins_update(member.id, coins - price)
                    order = in_order(member.id)  # Count order_number for scum_shopping_cart by discord id return 0 or 1
                    add_to_shoping_cart(member.id, member.name, players_info(member.id)[3], order_number, btn)
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

            if btn == 'add_to_cart':
                message = 'This command not available'
                await interaction.respond(content=message, ephemeral=True)
                return

            if btn == 'checkout':
                message = 'This command not available'
                await interaction.respond(content=message, ephemeral=True)
                return

        elif time <= shop_open:
            message = 'Drone is still unavailable : The shop is open from 10:00 to 24:00.'
            await interaction.respond(content=message)
        return False
