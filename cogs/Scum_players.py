import discord
from discord.ext import commands
from database.Players import exp_update
from database.Bank_db import plus_coins
from database.WWII_db import show_players, count_color_team
from discord_components import Button, ButtonStyle


class ScumPlayers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addexp')
    @commands.has_permissions(manage_roles=True)
    async def addexp_command(self, ctx, member: discord.Member, number: int):
        exp = exp_update(member.id, number)
        y_int = isinstance(exp, int)
        await ctx.reply(f'อัพเดทค่าประสบการณ์ให้กับ {member.display_name} จำนวน {number} เป็นที่เรียบร้อย',
                        mention_author=False)
        if y_int is True:
            await discord.DMChannel.send(member, f'คุณได้รับค่าประสบการณ์จำนวน {number} :'
                                                 f' ค่าประสบการณ์ปัจจุบันของคุณคือ {exp}')
        else:
            await discord.DMChannel.send(member, exp)

    @addexp_command.error
    async def addexp_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Your commands mission argument, Please verify again.', mention_author=False)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Your Role are used this commands.')

    @commands.command(name='addcoins')
    async def addcoins_command(self, ctx, member: discord.Member, number: int):
        coins = plus_coins(member.id, number)
        await ctx.reply(f'เติมเงินให้กับ {member.display_name} จำนวน {number} เป็นที่เรียบร้อย', mention_author=False)
        await discord.DMChannel.send(member, f'ระบบได้เติมเงินให้คุณจำนวน {number} ยอดเงินคงเหลือของคุณคือ {coins}')

    @addcoins_command.error
    async def addcoins_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Your commands mission argument, Please verify again.', mention_author=False)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Your Role are used this commands.')

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        btn = interaction.component.custom_id
        check_list = ["red_check", "blue_check", "all_check"]
        if btn in check_list:
            x = show_players(btn)
            y = count_color_team(btn)
            msg = f'📃**แสดงรายชื่อผู้เข้าร่วมกิจกรรม**\n```{x}\n\n==========='\
                  f'================\nจำนวนสมาชิกทีม RED : {y} คน```'
            await interaction.respond(content=msg)

    @commands.command(name='show_players')
    async def show_player(self, ctx):

        await ctx.send(
            file=discord.File('./img/the_battle.png'),
            components=[
                [
                    Button(style=ButtonStyle.red, label='RED CHECK', emoji='⚔', custom_id='red_check'),
                    Button(style=ButtonStyle.blue, label='BLUE CHECK', emoji='⚔', custom_id='blue_check'),
                    Button(style=ButtonStyle.gray, label='ALL TEAM', emoji='⚔', custom_id='all_check')
                ]
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(ScumPlayers(bot))
