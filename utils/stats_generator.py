import json
import random

distribution = {1: [1, 3], 2: [4, 6], 3: [7, 9]}


def generate_stats(player_class):
    with open("data/battle/class_config.json", "r", encoding="utf-8") as config:
        config = json.load(config)

    weighting = config[player_class]
    _str_distribution = distribution_to_stat(weighting["_str"])
    _def_distribution = distribution_to_stat(weighting["_def"])
    _spd_distribution = distribution_to_stat(weighting["_spd"])

    return {"_str": _str_distribution, "_def": _def_distribution, "_spd": _spd_distribution}


def distribution_to_stat(rating):
    bounds = distribution[rating]
    return random.randint(bounds[0], bounds[1])
