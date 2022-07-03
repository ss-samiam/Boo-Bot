import discord
from discord.ext import commands
import json

from utils import repo


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, prefix=""):
        if prefix == "":
            prefix = repo.DEFAULT_PREFIX
        guild_id = str(ctx.guild.id)

        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes[guild_id] = prefix
        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=2)
        await ctx.send(f"Prefix has been set to: `{prefix}`")


def setup(bot):
    bot.add_cog(Prefix(bot))
