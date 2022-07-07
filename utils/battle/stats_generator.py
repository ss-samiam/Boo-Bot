import discord
import json
import random

from utils.battle import battle_constants


def check_user_exist(guild_id, user_id):
    with open("data/stats.json", "r", encoding="utf-8") as file:
        user_details = json.load(file)
    for entry in user_details:
        if guild_id == entry["guild_id"] and user_id == entry["user_id"]:
            return True
    return False


def generate_embed(embed_colour):
    with open("data/battle/class_config.json", "r", encoding="utf-8") as config:
        config = json.load(config)

    embed = discord.Embed(title="Please choose your class", colour=embed_colour)

    for _class, details in config.items():
        embed.add_field(name=f"{details['emoji']} {_class.title()}",
                        value=f"{details['description']}\n"
                              f"STR {rating_to_stars(details['_str'])} "
                              f"DEF {rating_to_stars(details['_def'])} "
                              f"SPD {rating_to_stars(details['_spd'])}",
                        inline=False)

    embed.set_footer(text="Your base stats are randomly allocated with weighting depending on the class you have selected")
    return embed


def emoji_to_class_dict():
    with open("data/battle/class_config.json", "r", encoding="utf-8") as config:
        config = json.load(config)

    result = {}
    for _class, details in config.items():
        result[details["emoji"]] = _class
    return result


def class_to_emoji_dict():
    with open("data/battle/class_config.json", "r", encoding="utf-8") as config:
        config = json.load(config)

    result = {}
    for _class, details in config.items():
        result[_class] = details["emoji"]
    return result


def generate_stats(player_class):
    with open("data/battle/class_config.json", "r", encoding="utf-8") as config:
        config = json.load(config)

    weighting = config[player_class]
    _str_distribution = distribution_to_stat(weighting["_str"])
    _def_distribution = distribution_to_stat(weighting["_def"])
    _spd_distribution = distribution_to_stat(weighting["_spd"])

    return {"_str": _str_distribution, "_def": _def_distribution,
            "_spd": _spd_distribution}


def distribution_to_stat(rating):
    bounds = battle_constants.BASE_STATS_DISTRIBUTION[rating]
    return random.randint(bounds[0], bounds[1])


def rating_to_stars(rating):
    filled = "★" * rating
    empty = "☆" * (3 - rating)
    return filled + empty
