import discord
from discord.ext import commands
import random


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, message):
        user_id = ctx.author.id
        user_name = self.bot.get_user(user_id).name
        dice_split = message.split("d")
        if len(dice_split) != 2:
            await ctx.send(f"Invalid die! Please provide a valid format: ``<optional: amount of die to be rolled>d<sides of the die>``")
        else:
            amount = dice_split[0]
            dice_type = dice_split[1]

            response = f"🎲 **{user_name.split('#', 1)[0]}** rolls a {dice_type}-sided die"
            result = f"And gets a **{random.randrange(int(dice_type))}**"
            if amount:
                response += f" {amount} times"
                for i in range(int(amount) - 1):
                    result += f", **{random.randrange(int(dice_type))}**"

            response += "."
            result += "!"
            await ctx.send(response)
            await ctx.send(result)


def setup(bot):
    bot.add_cog(Roll(bot))
