import discord

from utils import repo, image_generator
from discord.ext import commands
import random


class Images(commands.Cog):
    """Sends images of who/what the user specified"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wallpaper(self, ctx, *, arg):
        try:
            image = image_generator.Wallhaven.get_image(ctx, arg)
            embed_media = discord.Embed(color=random.choice(repo.COLOURS))
            embed_media.set_image(url=image)
            await ctx.send(embed=embed_media)
        except IndexError:
            user_id = ctx.author.id
            await ctx.send(f'<@{user_id}> I can\'t find who/what you are looking for. Please specify!')

    @commands.command()
    async def image(self, ctx, *, arg):
        image = image_generator.Zerochan.get_image(ctx, arg)
        if image:
            image = random.choice(image)
            embed_media = discord.Embed(color=random.choice(repo.COLOURS))
            embed_media.set_image(url=image)
            await ctx.send(embed=embed_media)
        else:
            user_id = ctx.author.id
            await ctx.send(f'<@{user_id}> I can\'t find who/what you are looking for. Please specify!')


def setup(bot):
    bot.add_cog(Images(bot))

