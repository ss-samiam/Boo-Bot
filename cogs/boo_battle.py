import discord
from discord.ext import commands
import json
import csv
import random

from utils import repo


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

        user_id = ctx.author.id
        target = self.bot.get_user(user_id)

        def check(reaction, user):
            return user == ctx.message.author

        user_id = ctx.message.author.id
        guild_id = ctx.message.guild.id

        selection = discord.Embed(title="Please choose your class", colour=random.choice(repo.COLOURS))
        selection.add_field(name="🏹 Ranger", value="A ranged and agile class\nSTR ★★☆ DEF ★☆☆ SPD ★★★", inline=False)
        selection.add_field(name="⚔ Knight", value="A melee class boasting heavy defenses\nSTR ★★☆ DEF ★★★ SPD ★☆☆", inline=False)
        selection.set_footer(text="Your base stats are randomly allocated with weighting depending on the class you have selected")
        class_selection = await ctx.send(embed=selection)
        await class_selection.add_reaction("🏹")
        await class_selection.add_reaction("⚔")
        reaction = await self.bot.wait_for("reaction_add", check=check)
        print(reaction)
        await ctx.send(f"You have chosen: {reaction[0]}")

        base = discord.Embed(title="Stats", colour=random.choice(repo.COLOURS))
        base.set_author(name=target.display_name, icon_url=target.avatar_url)
        base.add_field(name="STR", value=1, inline=True)
        base.add_field(name="DEF", value=2, inline=True)
        base.add_field(name="SPD", value=3, inline=True)
        await ctx.send(embed=base)

        await ctx.send("Do you wish to register? (y/n)")
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        print(msg)

        if msg.content == "y":
            await ctx.send("You have been registered!")
        else:
            await ctx.send("Registration has been cancelled.")


def setup(bot):
    bot.add_cog(Battle(bot))
