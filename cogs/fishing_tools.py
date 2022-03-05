import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

class FishingTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        
    @commands.command(name='fishing_pack')
    async def fishing_pack(self, ctx):
        await ctx.send(
            file=discord.File('./img/store/fishing_rod.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, label='GRAY SET', custom_id='gray_set'),
                    Button(style=ButtonStyle.blue, label='BLUE SET', custom_id='blue_set'),
                    Button(style=ButtonStyle.green, label='GREEN SET', custom_id='green_set'),
                    Button(style=ButtonStyle.red, label='RED SET', custom_id='red_set')
                ]
            ]
        )

def setup(bot):
    bot.add_cog(FishingTools(bot))