from discord.ext import commands
from Store.fishing_tools import FishingTools
from Store.Bayonet import Bayonet


class DiscordStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(DiscordStore(bot))
    bot.add_cog(FishingTools(bot))
    bot.add_cog(Bayonet(bot))
