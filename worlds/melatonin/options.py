from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions


class MaxStarCheck(Choice):
    """
    Determines the maximum star threshold which sends a check.
    """
    display_name = "Maximum Star Check"
    option_1 = 1
    option_2 = 2
    option_3 = 3
    default = 2


class IncludeHardMode(Toggle):
    """
    Determines if hard mode versions of dreams send checks.
    """
    display_name = "Include Hard Mode"


class RequiredStarPercent(Range):
    """
    Percentage of stars added to the pool required for goal (roughly).

    This affects every level's star cost.
    """
    range_start = 50
    range_end = 100
    default = 80
    display_name = "Required Star Percent"



melatonin_option_groups = [
    OptionGroup("General", [
        MaxStarCheck,
        IncludeHardMode,
        RequiredStarPercent
    ])
]

@dataclass
class MelatoninOptions(PerGameCommonOptions):
    max_star_check: MaxStarCheck
    include_hard_mode: IncludeHardMode
    required_star_percent: RequiredStarPercent