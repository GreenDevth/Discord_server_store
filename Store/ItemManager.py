from discord.ext import commands


class ItemsManager(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.command(name='check')
    async def check_command(self, ctx, arg: str):
        if ctx.channel.id != 925559937323659274:
            await ctx.reply('คุณควรใช้งานคำสั่งนี้ที่ห้อง <#925559937323659274>')
            return False
        elif ctx.author.guild_permissions.administrator:
            await ctx.reply('arg')
        else:
            await ctx.reply('arg')

    @check_command.error
    async def check_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param))
