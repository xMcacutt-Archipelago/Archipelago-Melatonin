from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MelatoninWorld

from .data import *


def set_rules(world: MelatoninWorld):
    stars_required = int((world.options.required_star_percent.value / 100) * world.stars)
    stars_per_level = stars_required // LOCKED_LEVEL_COUNT
    night_index = 1
    dream_index = 0
    for night, dream_list in world.level_map.items():
        for dream in dream_list:
            if dream.type == NORMAL:
                entrance = world.get_entrance(f"Night {night_index} -> {dream.name}")
                stars_required = stars_per_level * dream_index
                entrance.access_rule = lambda state, n=stars_required: state.has(STAR, world.player, n)
                #print(f"{stars_required} Stars Required for Dream: {dream.name}")
                dream_index += 1
            if dream.type == FINAL:
                entrance = world.get_entrance(f"Night {night_index} -> {dream.name}")
                stars_required = stars_per_level * dream_index
                #print(f"{stars_required} Stars Required for Dream: {dream.name}")
                entrance.access_rule = lambda state, n=stars_required: state.has(STAR, world.player, n)
                dream_index += 1
        night_index += 1