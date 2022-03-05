import discord
from discord.ext import commands
from discord_components import DiscordComponents
from config.config import config_cogs, get_token
bot = commands.Bot(command_prefix='$')
bot.remove_command('help')
DiscordComponents(bot)

token = get_token(8)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Discord Store'))

config_cogs(bot)
bot.run(token)

