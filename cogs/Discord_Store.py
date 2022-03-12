from discord.ext import commands
from Store.fishing_tools import FishingTools
from Store.Bayonet import Bayonet


class DiscordStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='buy')
    async def buy_command(self, ctx, arg: str):
        await ctx.reply('⚠ This command is not available in Store', mention_author=False)

    @buy_command.error
    async def buy_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument **{}**'.format(error.param), mention_author=False)


def setup(bot):
    bot.add_cog(DiscordStore(bot))
    bot.add_cog(FishingTools(bot))
    bot.add_cog(Bayonet(bot))
