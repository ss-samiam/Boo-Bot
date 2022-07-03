import discord
from discord.ext import commands
import random
import re

from utils import repo


class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, message):
        ask_responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Yes.",
            "Signs point to yes.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
            "Highly unlikely.",
            "No."
        ]
        await ctx.send(f"🎱 {random.choice(ask_responses)}")

    @commands.command()
    async def choose(self, ctx, *, message):
        choices = re.split(', |,', message)
        print(list(filter(None, choices)))
        choice = random.choice(list(filter(None, choices)))
        choose_responses = [
            f"**{choice}** 100%",
            f"All signs point to **{choice}**",
            f"Definitely **{choice}**!",
            f"Hmmm, leaning towards **{choice}**...",
            f"**{choice}** obviously, duh",
            f"It has to be **{choice}**!",
            f"I love **{choice}**!",
            f"**{choice}** is the best choice",
            f"**{choice}** without a doubt!",
            f"Pick **{choice}**!",
            f"You must be dreaming if you aren't going with **{choice}**!",
        ]
        await ctx.send(random.choice(choose_responses))


def setup(bot):
    bot.add_cog(Ask(bot))
