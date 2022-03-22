import discord
from discord.ext import commands
from database.Store_db import check_stock, check_pack, list_cate, list_pack


class ItemsManager(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.command(name='check')
    async def check_command(self, ctx, arg: str):
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
                        name=f"{pack[0]}",
                        value=f"คงเหลือในสต๊อค : ```css\n{pack[2]}\n```",
                        inline=False
                    )
                    embed.add_field(
                        name='ราคาปัจจุบัน',
                        value=f"```css\n{pack[3]}\n```",
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

    @commands.command(name='list_pack')
    @commands.has_permissions(manage_roles=True)
    async def list_pack_commands(self, ctx, arg: str):
        packs = list_pack(arg)
        for pack in packs:
            await ctx.send(f"Your pack name is ```ini\n{pack[0]}\n```")
