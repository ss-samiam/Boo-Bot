"""
Animal pics and GIFs
"""
import discord

from utils import repo, cat_generator
from discord.ext import commands
import random


class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """ Random images of cats"""
    @commands.command()
    async def cat(self, ctx):
        embed_media = discord.Embed(color=random.choice(repo.COLOURS))
        embed_media.set_image(url=cat_generator.adopt_cat())
        await ctx.send(embed=embed_media)

    """ Random images of anime cats"""
    @commands.command()
    async def nya(self, ctx):
        image = cat_generator.adopt_anime_cat()
        embed_media = discord.Embed(color=0xFFC0CB)
        embed_media.set_image(url=image)
        await ctx.send(embed=embed_media)


def setup(bot):
    bot.add_cog(Animals(bot))

