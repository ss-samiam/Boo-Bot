import discord
import json
from discord.ext import commands

with open("data/config.json", "r", encoding="utf-8") as config:
    config = json.load(config)


DEFAULT_PREFIX = config.get("default_prefix")


# Get prefixes
def get_prefix(bot, message):
    with open("data/prefixes.json", "r", encoding="utf-8") as prefixes:
        prefixes = json.load(prefixes)
    return prefixes.get(str(message.guild.id), DEFAULT_PREFIX)


# Get token
def get_token():
    return config.get("token")
