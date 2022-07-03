import discord
from discord.ext import commands
import json
import re
import random

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

    @commands.Cog.listener()
    async def on_message(self, message):
        # Performs reactions as defined in the config
        for trigger, reaction in repo.REACTIONS.items():
            if re.search(fr"\b({trigger})\b", message.content, re.IGNORECASE):
                for emoji in reaction:
                    await message.add_reaction(emoji)

        # Performs reactions to messages containing "league"
        if re.search(fr"\b(league)\b", message.content, re.IGNORECASE) and message.author.id != self.bot.user.id:
            league_response = [
                "League of Legends is bad please don't play it",
                "Have you ever considered touching grass instead?",
                "🤮",
                "I suggest you to do anything but play League",
                "Hey, that's good and all but don't touch that game please",
                "Think of the children!",
                "Yeah, how about no"
            ]
            await message.channel.send(random.choice(league_response))

        # Imagine.
        elif re.search(r"\b(imagine)\b", message.content, re.IGNORECASE) and message.author.id != self.bot.user.id:
            response = random.choice(["Imagine.", "> i m a g i n e"])
            await message.channel.send(response)

def setup(bot):
    bot.add_cog(Events(bot))
