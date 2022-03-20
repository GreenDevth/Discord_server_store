import random
from datetime import datetime

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from database.Bank_db import coins_update
from database.Shopping_Cart import *
from database.Store_db import *


class ServerStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reset')
    @commands.has_permissions(manage_roles=True)
    async def reset_stock_command(self, ctx, arg: str):
        if arg == 'stock':
            reset_stock()
            await ctx.reply('Reset Stock Successfully..', mention_author=False)
            await ctx.message.delete()

    @reset_stock_command.error
    async def reset_stock_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Only for Admin', mention_author=False)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)

    @commands.command(name='listpack')
    @commands.has_permissions(manage_roles=True)
    async def listpack_commands(self, ctx, arg: str):
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
                        Button(style=ButtonStyle.blue, label='ADD TO CART', emoji='🛒', disabled=True),
                        Button(style=ButtonStyle.red, label='CHECKOUT', emoji='💳', disabled=True)
                    ]
                ]
            )

    @listpack_commands.error
    async def listpack_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Only for Admin', mention_author=False)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)

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
                    Button(style=ButtonStyle.blue, label='ADD TO CART', emoji='🛒', disabled=True),
                    Button(style=ButtonStyle.red, label='CHECKOUT', emoji='💳', disabled=True)
                ]
            ]
        )

    @listitem_command.error
    async def listitem_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('You can not use this command', mention_author=False)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Mission required argument : {}'.format(error.param))

    @commands.command(name='listcate')
    @commands.has_permissions(manage_roles=True)
    async def listcate_command(self, ctx, arg: str):
        cate = listcate(arg)
        for x in cate:
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
                        Button(style=ButtonStyle.blue, label='ADD TO CART', emoji='🛒', disabled=True),
                        Button(style=ButtonStyle.red, label='CHECKOUT', emoji='💳', disabled=True)
                    ]
                ]
            )

    @listcate_command.error
    async def listcate_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('You can not use this command', mention_author=False)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Mission required argument : {}'.format(error.param))

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        buy_btn = interaction.component.custom_id
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
        shop_open = "00:00:00"
        level = item_level(buy_btn)
        player_lavel = players_info(member.id)[6]
        if shop_open <= time:
            stock = in_stock(buy_btn)
            if stock != 0:
                level = item_level(buy_btn)
                if player_lavel > level:
                    if buy_btn in btn_ist:
                        price = get_price(buy_btn)
                        title = get_title(buy_btn)
                        coins = players_info(member.id)[5]
                        if coins < price:
                            message = '⚠ : ยอดเงินของคุณไม่เพียงพอสำหรับสั่งซื้อ' \
                                      ' ยอดเงินของคุณทั้งหมดคือ ``${:,d}``'.format(coins)
                            await interaction.respond(content=message)
                            return
                        elif price <= coins:
                            message = f"กรุณารอสักครู่ ระบบกำลังเตรียมจัดส่ง **{title}** ให้คุณ"
                            await interaction.respond(content=message)
                            update_stock(buy_btn, stock - 1)
                            coins_update(member.id, coins - price)
                            order = in_order(member.id)
                            add_to_shoping_cart(
                                member.id, member.name,
                                players_info(member.id)[3],
                                order_number, buy_btn
                            )
                            if count == 0:
                                queue = check_queue()
                                checkout = '--run {}'.format(order_number)
                                await cmd_channel.send(
                                    f'{member.mention}\n'
                                    f'```เลขที่ใบสั่งซื้อ {order_number} อยู่ระหว่างการจัดส่ง'
                                    f' จำนวนคิวจัดส่ง {order}/{queue}```')
                                await run_channel.send(checkout)
                                print('run command to send package to player')
                                return
                            else:
                                queue = check_queue()
                                await cmd_channel.send(
                                    f'{member.mention}\n'
                                    f'```เลขที่ใบสั่งซื้อ {order_number} อยู่ระหว่างการจัดส่ง'
                                    f' จำนวนคิวจัดส่ง {order}/{queue}```', mention_author=False)
                                print('send information without run command')
                                return
                else:
                    await interaction.respond(content='⚠ **Level** ของคุณไม่เพียงพอสำหรับคำสั่งซื้อนี้')
                    return

            elif stock == 0:
                await interaction.respond(content='❌ Out of Stock')
                return

        elif time <= shop_open:
            message = 'Drone is still unavailable : The shop is open from 10:00 to 24:00.'
            await interaction.respond(content=message)
        return False
