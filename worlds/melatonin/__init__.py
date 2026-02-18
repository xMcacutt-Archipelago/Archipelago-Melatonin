from operator import truediv
from typing import Dict, Optional, Any, TextIO

from BaseClasses import Tutorial, MultiWorld, ItemClassification, Item, Location
from worlds.AutoWorld import WebWorld, World
from worlds.melatonin.data import *
from worlds.melatonin.items import melatonin_item_dict, create_items, MelatoninItem
from worlds.melatonin.locations import melatonin_location_dict
from worlds.melatonin.options import *
from worlds.melatonin.regions import create_regions
from worlds.melatonin.rules import set_rules


class MelatoninWeb(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Melatonin randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["xMcacutt", "DawntoldStories"]
    )

    tutorials = [setup_en]
    option_groups = melatonin_option_groups

class MelatoninWorld(World):
    """
    Melatonin is a rhythm game about dreams and reality merging together.
    It uses animations and sound cues to keep you on beat without any intimidating overlays or interfaces.
    Harmonize through a variety of dreamy levels containing surprising challenges, hand-drawn art, and vibrant music.
    """
    game = "Melatonin"
    options_dataclass = MelatoninOptions
    options: MelatoninOptions
    topology_present = True
    item_name_to_id = {item_name: item_data.code for item_name, item_data in melatonin_item_dict.items()}
    location_name_to_id = melatonin_location_dict
    # location_name_groups =

    web = MelatoninWeb()
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.level_map = {}
        self.item_pool = []
        self.stars = 0

    def generate_early(self):
        normal_levels = [level.name for night in melatonin_levels.values() for level in night if level.type == NORMAL]
        self.random.shuffle(normal_levels)
        self.level_map: dict[str, list[Dream]] = {
            "Night 1": [
                Dream(normal_levels[0], NORMAL),
                Dream(normal_levels[1], NORMAL),
                Dream(normal_levels[2], NORMAL),
                Dream(normal_levels[3], NORMAL),
                Dream(INDULGENCE, FINAL)
            ],
            "Night 2": [
                Dream(normal_levels[4], NORMAL),
                Dream(normal_levels[5], NORMAL),
                Dream(normal_levels[6], NORMAL),
                Dream(normal_levels[7], NORMAL),
                Dream(PRESSURE, FINAL)
            ],
            "Night 3": [
                Dream(normal_levels[8], NORMAL),
                Dream(normal_levels[9], NORMAL),
                Dream(normal_levels[10], NORMAL),
                Dream(normal_levels[11], NORMAL),
                Dream(MEDITATION, FINAL)
            ],
            "Night 4": [
                Dream(normal_levels[12], NORMAL),
                Dream(normal_levels[13], NORMAL),
                Dream(normal_levels[14], NORMAL),
                Dream(normal_levels[15], NORMAL),
                Dream(SETBACKS, FINAL)
            ],
            "Night 5": [
                Dream(NEWDAY, GOAL)
            ]
        }
        pass

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        create_items(self)

    def set_rules(self):
        set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region(f"Night 5", self.player)

    def fill_slot_data(self):
        # from Utils import visualize_regions
        # state = self.multiworld.get_all_state(False)
        # state.update_reachable_regions(self.player)
        # visualize_regions(self.get_region("Menu"), f"{self.player}_world.puml",
        #   show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player])
        normal_levels = [level.name for night in melatonin_levels.values() for level in night if level.type == NORMAL]
        remapped_levels = [level.name for night in self.level_map.values() for level in night if level.type == NORMAL]
        level_mapping = { normal_level.lower(): remapped_levels[idx].lower() for idx, normal_level in enumerate(normal_levels) }
        stars_per_level = self.stars * (self.options.required_star_percent.value / 100) // LOCKED_LEVEL_COUNT
        return {
            "StarCount": self.stars,
            "StarPercent": self.options.required_star_percent.value,
            "IncludeHard": self.options.include_hard_mode.value,
            "MaxStarCheck": self.options.max_star_check.value,
            "StarsPerLevel": int(stars_per_level),
            "LevelMapping": level_mapping
        }

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"Stars required per level: {self.stars * (self.options.required_star_percent.value / 100) // LOCKED_LEVEL_COUNT}")

    def handle_ut_yamless(self, slot_data: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
        if not slot_data \
                and hasattr(self.multiworld, "re_gen_passthrough") \
                and isinstance(self.multiworld.re_gen_passthrough, dict) \
                and self.game in self.multiworld.re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[self.game]
        if not slot_data:
            return None
        self.options.include_hard_mode.value = slot_data["IncludeHard"]
        self.options.max_star_check.value = slot_data["MaxStarCheck"]
        self.options.required_star_percent.value = slot_data["StarPercent"]
        self.level_map = slot_data["LevelMapping"]
        return slot_data

    def create_item(self, name: str):
        item_info = melatonin_item_dict[name]
        return MelatoninItem(name, item_info.classification, item_info.code, self.player)

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        new_hint_data = {}

        normal_levels = [level.name for night in melatonin_levels.values() for level in night if level.type == NORMAL]
        remapped_levels = [level.name for night in self.level_map.values() for level in night if level.type == NORMAL]
        level_mapping = { normal_level.lower(): remapped_levels[idx].lower() for idx, normal_level in enumerate(normal_levels) }
        level_mapping[INDULGENCE] = INDULGENCE
        level_mapping[SETBACKS] = SETBACKS
        level_mapping[PRESSURE] = PRESSURE
        level_mapping[MEDITATION] = MEDITATION
        for location in self.get_locations():
            origin_dream: str
            origin_night: str
            region_name: str = location.parent_region.name
            for og_dream, mp_dream in level_mapping.items():
                if f"dream: {mp_dream.lower()}" == region_name.lower():
                    origin_dream = og_dream
                    break
            origin_night = location.parent_region.entrances[0].parent_region.name

            #print(f"{location.name} is at Dream: {origin_dream.lower().capitalize()} on {origin_night.lower().capitalize()}")

            new_hint_data[location.address] = f"Dream: {origin_dream.lower().capitalize()} on {origin_night.lower().capitalize()}"

        hint_data[self.player] = new_hint_data

    def get_filler_item_name(self) -> str:
        return STAR