import discord
from discord.ext import commands
import json

from utils import repo


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Boo Bot is online.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes[str(guild.id)] = repo.DEFAULT_PREFIX
        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=2)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes.pop(str(guild.id))
        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=2)


def setup(bot):
    bot.add_cog(Events(bot))
