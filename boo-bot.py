import discord
import os
import asyncio
from discord.ext import commands
from utils import repo

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=repo.get_prefix, intents=intents)


# Loads all cogs
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(repo.get_token(), bot=True, reconnect=True)

