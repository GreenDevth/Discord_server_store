from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.Players import players_info
class Location(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='home')
    async def home_location(self, ctx):
        player = players_info(ctx.author.id)
        await ctx.send(
            '.set #Teleport 240610.469 82449.469 26973.654 {}'.format(player[3])
        )

def setup(bot):
    bot.add_cog(Location(bot))