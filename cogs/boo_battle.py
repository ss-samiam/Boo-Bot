import discord
from discord.ext import commands
import csv
import random

from utils import repo
from utils.battle import stats_generator
from utils.battle import battle_constants


def check_user_exist(guild_id, user_id):
    with open("data/stats.csv", "r") as file:
        reader = csv.DictReader(file, fieldnames=battle_constants.FIELDNAMES)
        for row in reader:
            if str(guild_id) == row["Guild_ID"] and str(user_id) == row["User_ID"]:
                return True
        return False


class Player:
    def __init__(self, name, stats):
        self.name = name
        self.health = 10
        self._str = stats["Strength"]
        self._def = stats["Defense"]
        self._spd = stats["Speed"]
        self.xp = stats["XP"]
        self.skills = stats["Skills"]
        # xp = (level/x)^y
        # level = (xp**(1/y)) * x

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health

    def get_str(self):
        return self._str

    def get_def(self):
        return self._def

    def get_spd(self):
        return self._str

    def get_xp(self):
        return self.xp

    def get_level(self):
        return int(((self.xp**(1/battle_constants.XP_Y)) * battle_constants.XP_X) // 1)

    def take_dmg(self, damage):
        self.health = self.health - damage

    def attack(self, opponent):
        damage = self.get_str() * (100/(100 + opponent.get_def()))
        opponent.take_dmg(damage)
        return damage


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def battle(self, ctx, target=None):
        guild_id = ctx.message.guild.id
        guild = self.bot.get_guild(guild_id)
        caller = ctx.author
        if not check_user_exist(guild_id, caller.id):
            await ctx.send("You are not registered! Please register using the ``register`` command")
            return

        if target is None:
            await ctx.send("Please tag a user to initiate a fight with them.")
            return
        elif len(ctx.message.mentions) > 2:
            await ctx.send("You can only fight with another person!")
            return

        target = guild.get_member(int(target[2:-1]))
        if caller == target:
            await ctx.send("You can't fight yourself") # Add some random choices
            return

        if not check_user_exist(guild_id, target.id):
            await ctx.send(f"{target.display_name} is not registered! Please register using the ``register`` command")

        # Load stats of caller and target
        with open("data/stats.csv", mode="r", newline="") as file:
            reader = csv.DictReader(file, fieldnames=battle_constants.FIELDNAMES)
            for row in reader:
                if str(guild_id) == row["Guild_ID"] and str(caller.id) == row["User_ID"]:
                    caller_stats = row
                if str(guild_id) == row["Guild_ID"] and str(target.id) == row["User_ID"]:
                    target_stats = row

        caller_name = caller.display_name
        caller_class = caller_stats["Class"]
        caller_str = int(caller_stats["Strength"])
        caller_def = int(caller_stats["Defense"])
        caller_spd = int(caller_stats["Speed"])
        caller_player = Player(caller_name, caller_stats)

        target_name = target.display_name
        target_class = target_stats["Class"]
        target_str = int(target_stats["Strength"])
        target_def = int(target_stats["Defense"])
        target_spd = int(target_stats["Speed"])
        target_player = Player(target_name, target_stats)

        winner = None
        while True:

            # Caller attacks first
            if caller_spd > target_spd:
                fst_attacker = caller_player
                snd_attacker = target_player
            # Target attacks first
            else:
                fst_attacker = target_player
                snd_attacker = caller_player

            fst_damage = fst_attacker.attack(snd_attacker)
            await ctx.send(f"**{fst_attacker.name}** attacks **{snd_attacker.name}**")
            await ctx.send(f"**{fst_attacker.name}** dealt **{round(fst_damage, 1)}** damage!")
            await ctx.send(f"**{fst_attacker.name}**'s Health ♡: **{round(fst_attacker.health, 1)}** | **{snd_attacker.name}**'s Health ♡: **{round(snd_attacker.health, 1)}**")

            if snd_attacker.health <= 0:
                winner = fst_attacker
                break

            snd_damage = snd_attacker.attack(fst_attacker)
            await ctx.send(f"**{snd_attacker.name}** attacks **{fst_attacker.name}**")
            await ctx.send(f"**{snd_attacker.name}** dealt **{round(snd_damage, 1)}** damage!")
            await ctx.send(f"**{fst_attacker.name}**'s Health ♡: **{round(fst_attacker.health, 1)}** | **{snd_attacker.name}**'s Health ♡: **{round(snd_attacker.health, 1)}**")

            if fst_attacker.health <= 0:
                winner = snd_attacker
                break

        await ctx.send("**Battle is finished**")
        await ctx.send(f"**{winner.name}** wins!")


    @commands.command()
    async def stats(self, ctx, target=None):
        guild_id = ctx.message.guild.id
        user_id = ctx.message.author.id

        if target is None:
            target = ctx.message.author

        display_stats = {}
        with open("data/stats.csv", mode="r", newline="") as file:
            reader = csv.DictReader(file, fieldnames=battle_constants.FIELDNAMES)
            for row in reader:
                if row["Guild_ID"] == str(guild_id) and row["User_ID"] == str(target.id):
                    display_stats = row
                    break

        if display_stats:
            # Embed stats
            stats = discord.Embed(title="Stats", colour=random.choice(repo.COLOURS))
            stats.set_author(name=target.display_name, icon_url=target.avatar_url)
            class_emoji = stats_generator.class_to_emoji_dict()[display_stats["Class"]]
            stats.add_field(name="Class", value=f"{class_emoji} {display_stats['Class'].title()}", inline=False)
            stats.add_field(name="STR", value=display_stats["Strength"], inline=True)
            stats.add_field(name="DEF", value=display_stats["Defense"], inline=True)
            stats.add_field(name="SPD", value=display_stats["Speed"], inline=True)
            await ctx.send(embed=stats)
        else:
            await ctx.send("User not registered, please register using the ``register`` command")

    @commands.command()
    async def register(self, ctx):
        target = self.bot.get_user(ctx.author.id)
        guild_id = ctx.message.guild.id
        user_id = ctx.message.author.id

        # Check if user wants to re-register if they already registered
        user_exist = check_user_exist(guild_id, user_id)
        if user_exist:
            await ctx.send("You have already registered, do you wish to register again? (y/n)")
            again_msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if again_msg.content not in ["y", "Y"]:
                await ctx.send("The procedure has been stopped.")
                return

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
        _str = stats["_str"]
        _def = stats["_def"]
        _spd = stats["_spd"]
        player_stats = {"Guild_ID": guild_id, "User_ID": user_id, "Class": _class, "Strength": _str, "Defense": _def, "Speed": _spd}

        # Embed stats
        base = discord.Embed(title="Stats", colour=embed_colour)
        base.set_author(name=target.display_name, icon_url=target.avatar_url)
        base.add_field(name="Class", value=f"{reaction.emoji} {_class.title()}", inline=False)
        base.add_field(name="STR", value=_str, inline=True)
        base.add_field(name="DEF", value=_def, inline=True)
        base.add_field(name="SPD", value=_spd, inline=True)
        await ctx.send(embed=base)

        # Registration confirmation
        await ctx.send("Do you wish to register? (y/n)")
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content in ["y", "Y"]:
            new_rows = []
            with open("data/stats.csv", "r") as file:
                reader = csv.DictReader(file, fieldnames=battle_constants.FIELDNAMES)
                # Update stats if the user already exists
                for row in reader:
                    if row["Guild_ID"] == str(guild_id) and row["User_ID"] == str(user_id):
                        row = player_stats
                    new_rows.append(row)

                # Add to list if user has never registered before
                if not user_exist:
                    new_rows.append(player_stats)
                await ctx.send("You have been registered!")

            # Write the updated data to file.
            with open("data/stats.csv", "w", newline="") as output:
                writer = csv.DictWriter(output, fieldnames=battle_constants.FIELDNAMES)
                writer.writerows(new_rows)
        else:
            await ctx.send("Registration has been cancelled.")


def setup(bot):
    bot.add_cog(Battle(bot))
