import discord
import json
from discord.ext import commands

with open("data/config.json", "r", encoding="utf-8") as config:
    config = json.load(config)


DEFAULT_PREFIX = config.get("default_prefix")
COLOURS = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F,
           0x800000, 0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585,
           0xFFB6C1, 0x00CED1]  # Colours of embed borders


# Get prefixes
def get_prefix(bot, message):
    with open("data/prefixes.json", "r", encoding="utf-8") as prefixes:
        prefixes = json.load(prefixes)
    return prefixes.get(str(message.guild.id), DEFAULT_PREFIX)


# Get token
def get_token():
    return config.get("token")
