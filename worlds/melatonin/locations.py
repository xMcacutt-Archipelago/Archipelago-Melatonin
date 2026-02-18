from worlds.melatonin import melatonin_levels



def generate_locations():
    loc_dict = {}
    loc_id = 0x100
    for night, dream_list in melatonin_levels.items():
        for dream in dream_list:
            if dream.type == "Goal":
                continue
            for star_index in range(3):
                star_pluralisation = "Star" if star_index == 0 else "Stars"
                loc_dict[f"Dream: {dream.name} - {star_index + 1} {star_pluralisation}"] = loc_id
                loc_id += 1
            for ring_index in range(3):
                ring_pluralisation = "Ring" if ring_index == 0 else "Rings"
                loc_dict[f"Dream: {dream.name} (Hard) - {ring_index + 1} {ring_pluralisation}"] = loc_id
                loc_id += 1
    return loc_dict


melatonin_location_dict = generate_locations()