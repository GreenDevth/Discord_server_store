import discord
from discord.ext import commands

from database.Store_db import check_stocks, check_pack, list_cate, list_pack, check_cate, check_stock, update_stocks, \
    update_item_cmd, get_item_info_by_cmd, check_cmd


class ItemsManager(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.command(name='check_cate')
    async def check_command(self, ctx, arg: str):
        if ctx.channel.id == 925559937323659274 or ctx.author.guild_permissions.administrator:
            if check_cate(arg) == 0:
                await ctx.reply(f'ไม่พบข้อมูล {arg} ในฐานข้อมูล โปรดตรวจสอบความถูกต้อง..', mention_author=False)
            else:
                packs = check_stocks(arg)

                embed = discord.Embed(
                    title=f'รายการสินค้าประเภท {arg.upper()}',
                    colour=discord.Colour.green()
                )
                for pack in packs:
                    embed.add_field(
                        name="สินค้า",
                        value=f'```bash\n{pack[0]}\n```',
                        inline=False
                    )
                    embed.add_field(
                        name="คงเหลือ",
                        value=f"```css\n{pack[2]}\n```"
                    )
                    embed.add_field(
                        name='ราคาปัจจุบัน',
                        value=f"```css\n{pack[3]}\n```"
                    )

                await ctx.reply(
                    embed=embed,
                    mention_author=False
                )

        elif ctx.author.guild_permissions.administrator:
            await ctx.reply('arg')
        else:
            await ctx.reply('คุณควรใช้งานคำสั่งนี้ที่ห้อง <#955801360832528386>', mention_author=False)

    @check_command.error
    async def check_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)

    @commands.command(name='check_pack')
    async def checks_command(self, ctx, arg: str):
        if ctx.channel.id == 925559937323659274 or ctx.author.guild_permissions.administrator:
            if check_pack(arg) == 0:
                await ctx.reply(f'ไม่พบข้อมูล {arg} ในฐานข้อมูล โปรดตรวจสอบความถูกต้อง..', mention_author=False)
            else:
                packs = check_stock(arg)

                embed = discord.Embed(
                    title=f'รายการสินค้าประเภท {arg.upper()}',
                    colour=discord.Colour.green()
                )
                for pack in packs:
                    embed.add_field(
                        name="สินค้า",
                        value=f'```bash\n{pack[0]}\n```',
                        inline=False
                    )
                    embed.add_field(
                        name="คงเหลือ",
                        value=f"```css\n{pack[2]}\n```"
                    )
                    embed.add_field(
                        name='ราคาปัจจุบัน',
                        value=f"```css\n{pack[3]}\n```"
                    )

                await ctx.reply(
                    embed=embed,
                    mention_author=False
                )

        elif ctx.author.guild_permissions.administrator:
            await ctx.reply('arg')
        else:
            await ctx.reply('คุณควรใช้งานคำสั่งนี้ที่ห้อง <#955801360832528386>', mention_author=False)

    @checks_command.error
    async def checks_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)

    @commands.command(name='list_cate')
    @commands.has_permissions(manage_roles=True)
    async def list_cate_commands(self, ctx):
        cates = list_cate()
        embed = discord.Embed(
            title="Item list by Category",
            description='Coppy Category name and type $list_pack your category name and enter for list item pack',
            colour=discord.Colour.green(),
        )
        for cate in cates:
            embed.add_field(name='Category Name', value=f'```ini\n{cate[0]}\n```')
        await ctx.send(embed=embed)

    @list_cate_commands.error
    async def list_cate_commands_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)

    @commands.command(name='list_pack')
    @commands.has_permissions(manage_roles=True)
    async def list_pack_commands(self, ctx, arg: str):
        packs = list_pack(arg)
        for pack in packs:
            await ctx.send(f"Your pack name is ```ini\n{pack[0]}\n```")

    @list_pack_commands.error
    async def list_pack_commands_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)

    @commands.command(name="reset_stock")
    @commands.has_permissions(manage_roles=True)
    async def reset_stock(self, ctx, arg: str):
        if arg == "true":
            update = update_stocks()
            await ctx.reply(f'{update}', mention_author=False)

    @reset_stock.error
    async def reset_stock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)

        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Only for Admin command!!!', mention_author=False)

    @commands.command(name='fill')
    @commands.has_permissions(manage_roles=True)
    async def fill_stock_command(self, ctx, cmd: str, amount: int):
        """ fill item stock by commands """
        check = check_cmd(cmd)[0]
        if check != 0:
            update_item_cmd(cmd, amount)
            item = get_item_info_by_cmd(cmd)
            await ctx.reply(f'Update stock for **{item[1]}** successfully.', mention_author=False)
        elif check == 0:
            await ctx.reply(f"ไม่พบรายการสินค้า `` {cmd} `` ในระบบ", mention_author=False)

    @fill_stock_command.error
    async def fill_stock_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)

        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Only for Admin command!!!', mention_author=False)

    @commands.command(name='check_stock')
    async def check_stock(self, ctx, cmd: str):
        check = check_cmd(cmd)[0]
        print(type(check))
        if check != 0:
            item = get_item_info_by_cmd(cmd)
            embed = discord.Embed(
                title=f'{item[1]}',
                color=discord.Colour.green()
            )
            embed.set_image(url=f'{item[8]}')
            embed.add_field(name="IN STOCK", value=f'```css\n{item[9]}\n```'),
            embed.add_field(name="LEVEL REQUIRE", value=f'```css\n{item[10]}\n```')
            embed.add_field(name="PRICE", value='```css\n${:,d}\n```'.format(item[5]))
            await ctx.channel.send(embed=embed)
        elif check == 0:
            await ctx.reply(f"ไม่พบรายการสินค้า `` {cmd} `` ในระบบ", mention_author=False)

    @check_stock.error
    async def check_stock_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument *item command*', mention_author=False)
