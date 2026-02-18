from dataclasses import dataclass

FOOD = "Food"
TECH = "Tech"
SHOPPING = "Shopping"
FOLLOWERS = "Followers"
INDULGENCE = "Indulgence"
EXERCISE = "Exercise"
WORK = "Career"
MONEY = "Money"
DATING = "Dating"
PRESSURE = "Pressure"
TIME = "Time"
MIND = "Mind"
SPACE = "Space"
NATURE = "Nature"
MEDITATION = "Mediation"
STRESS = "Stress"
DESIRES = "Desires"
PAST = "Past"
FUTURE = "Future"
SETBACKS = "Setbacks"
NEWDAY = "New Day"

SCORE = "Score Mode"
HARD = "Hard Mode"

STAR = "Star"
NORMAL = "Normal"
FINAL = "Final"
GOAL = "Goal"

LOCKED_LEVEL_COUNT = 19


@dataclass
class Dream:
    name: str
    type: str


melatonin_levels: dict[str, list[Dream]] = {
    "Night 1": [
        Dream(FOOD, NORMAL),
        Dream(TECH, NORMAL),
        Dream(SHOPPING, NORMAL),
        Dream(FOLLOWERS, NORMAL),
        Dream(INDULGENCE, FINAL)
    ],
    "Night 2": [
        Dream(EXERCISE, NORMAL),
        Dream(WORK, NORMAL),
        Dream(MONEY, NORMAL),
        Dream(DATING, NORMAL),
        Dream(PRESSURE, FINAL)
    ],
    "Night 3": [
        Dream(TIME, NORMAL),
        Dream(MIND, NORMAL),
        Dream(SPACE, NORMAL),
        Dream(NATURE, NORMAL),
        Dream(MEDITATION, FINAL)
    ],
    "Night 4": [
        Dream(STRESS, NORMAL),
        Dream(PAST, NORMAL),
        Dream(FUTURE, NORMAL),
        Dream(DESIRES, NORMAL),
        Dream(SETBACKS, FINAL)
    ],
    "Night 5": [
        Dream(NEWDAY, GOAL)
    ]
}