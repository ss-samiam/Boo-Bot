import discord
from discord.ext import commands
import json
import csv
import random

from utils import repo
from utils import stats_generator


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx, target=None):
        found = False
        if target is None:
            target = ctx.message.author.id

        with open("data/stats.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for line in reader:
                try:
                    if line[0] == str(target.id):
                        found = True
                        strength = int(line[1])
                        defense = int(line[2])
                        speed = int(line[3])
                        break
                except:
                    found = False

        if found:
            embed = discord.Embed(title="Fighter Stats", colour=random.choice(repo.COLOURS))
            embed.set_author(name=target.display_name, icon_url=target.avatar_url)
            embed.add_field(name="STR", value=strength, inline=True)
            embed.add_field(name="DEF", value=defense, inline=True)
            embed.add_field(name="SPD", value=speed, inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"User not registered, please register using the ``register`` command")

    @commands.command()
    async def register(self, ctx):
        target = self.bot.get_user(ctx.author.id)
        user_id = ctx.message.author.id
        guild_id = ctx.message.guild.id

        # Generate class selection embed
        class_dict = stats_generator.emoji_to_class_dict()
        embed_colour = random.choice(repo.COLOURS)
        selection = stats_generator.generate_embed(embed_colour)
        class_selection = await ctx.send(embed=selection)

        # Generate class options with reactions
        for class_emoji, class_name in class_dict.items():
            await class_selection.add_reaction(class_emoji)
        reaction, user = await self.bot.wait_for("reaction_add", check=lambda r, u: u == ctx.message.author)
        await ctx.send(f"You have chosen: {reaction.emoji}")

        # Generate stats
        _class = class_dict[reaction.emoji]
        stats = stats_generator.generate_stats(_class)

        # Embed stats
        base = discord.Embed(title="Stats", colour=embed_colour)
        base.set_author(name=target.display_name, icon_url=target.avatar_url)
        base.add_field(name="Class", value=_class.title(), inline=False)
        base.add_field(name="STR", value=stats["_str"], inline=True)
        base.add_field(name="DEF", value=stats["_def"], inline=True)
        base.add_field(name="SPD", value=stats["_spd"], inline=True)
        await ctx.send(embed=base)

        # Registration confirmation
        await ctx.send("Do you wish to register? (y/n)")
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content == "y":
            await ctx.send("You have been registered!")
        else:
            await ctx.send("Registration has been cancelled.")


def setup(bot):
    bot.add_cog(Battle(bot))
