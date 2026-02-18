from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from BaseClasses import Region, Location, Entrance
from worlds.melatonin import melatonin_levels, FINAL, GOAL, NORMAL

if TYPE_CHECKING:
    from . import MelatoninWorld


def create_location(world, region: Region, name: str, code: int):
    location = Location(world.player, name, code, region)
    region.locations.append(location)


def create_region(world, name: str):
    region = Region(name, world.player, world.multiworld)
    world.multiworld.regions.append(region)
    return region


def connect_regions(world, from_name: str, to_name: str, entrance_name: str):
    from_region = world.get_region(from_name)
    to_region = world.get_region(to_name)
    entrance = from_region.connect(to_region, entrance_name)
    return entrance


def create_regions(world: MelatoninWorld):
    create_region(world, "Menu")

    for i in range(5):
        create_region(world, f"Night {i + 1}")
    connect_regions(world, "Menu", "Night 1", f"Menu -> Night 1")

    for i in range (5):
        night_index = i + 1
        night = f"Night {night_index}"
        for dream in world.level_map[night]:
            dream_name = f"Dream: {dream.name}"
            dream_region = create_region(world, dream_name)
            if dream.type != GOAL:
                for star_index in range(world.options.max_star_check.value):
                    star_pluralisation = "Star" if star_index == 0 else "Stars"
                    loc_name = f"{dream_name} - {star_index + 1} {star_pluralisation}"
                    create_location(world, dream_region, loc_name, world.location_name_to_id[loc_name])
                    if world.options.include_hard_mode:
                        ring_pluralisation = "Ring" if star_index == 0 else "Rings"
                        loc_name = f"{dream_name} (Hard) - {star_index + 1} {ring_pluralisation}"
                        create_location(world, dream_region, loc_name, world.location_name_to_id[loc_name])
            connect_regions(world, night, dream_name, f"{night} -> {dream.name}")
            if dream.type == FINAL:
                connect_regions(world, dream_name, f"Night {night_index + 1}", f"{dream_name} -> Night {night_index + 1}")