from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from BaseClasses import Item, ItemClassification
from worlds.melatonin.data import *

if TYPE_CHECKING:
    from . import MelatoninWorld


class MelatoninItem(Item):
    game: str = "Melatonin"


def create_single(name: str, world, item_class: ItemClassification = ItemClassification.filler):
    world.item_pool.append(MelatoninItem(name, item_class, melatonin_item_dict[name].code, world.player))


def create_multiple(name: str, amount: int, world, item_class: ItemClassification = ItemClassification.filler):
    for i in range(amount):
        create_single(name, world, item_class)


def create_items(world: MelatoninWorld):
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))
    remaining_locations = total_location_count - len(world.item_pool)
    world.stars = remaining_locations
    create_multiple(STAR, world.stars, world, melatonin_item_dict[STAR].classification)
    world.multiworld.itempool += world.item_pool


@dataclass
class ItemData:
    code: Optional[int]
    classification: ItemClassification


melatonin_item_dict = {
    f"{STAR}": ItemData(0x100, ItemClassification.progression_skip_balancing)
}