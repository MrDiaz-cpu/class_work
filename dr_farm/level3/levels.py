"""Starting fields, star thresholds and rules for the four public levels."""
FILES = ("tutorial.py", "level1.py", "level2.py", "level3.py")
NAMES = ("Tutorial", "Harvest", "Plant", "Timing")
RULES = [
    {"auto_replant": True, "planting_enabled": False, "timing_required": False},
    {"auto_replant": True, "planting_enabled": False, "timing_required": False},
    {"auto_replant": False, "planting_enabled": True, "timing_required": False},
    {"auto_replant": False, "planting_enabled": True, "timing_required": True},
]


def planted(names, target, best):
    return {"plots": [(name, 0) for name in names.split()], "target": target, "best": best}


def empty(count, bag, target, best):
    return {"plots": [("empty", 0)] * count, "target": target, "best": best,
            "seeds": dict(zip(("radish", "carrot", "corn", "pumpkin"), bag))}


FIELDS = [
    {"challenge": planted("radish", 1, 3)},
    {"challenge": planted("radish carrot corn radish pumpkin carrot", 10, 13),
     "remix": planted("corn radish radish pumpkin carrot radish corn carrot", 14, 18)},
    {"challenge": empty(6, (3, 3, 2, 1), 15, 24), "remix": empty(8, (4, 4, 3, 1), 20, 31)},
    {"challenge": empty(6, (4, 3, 3, 3), 15, 36), "remix": empty(8, (6, 4, 4, 3), 20, 45)},
]


def layout(level, field):
    if type(level) is not int or level not in range(len(FILES)) or field not in FIELDS[level]:
        raise ValueError("Choose a level and field from the menu.")
    return dict(FIELDS[level][field], **RULES[level])


def stars(score, target, best, eligible=True):
    if not eligible or score < target:
        return 0
    if score >= best:
        return 3
    return 2 if 2 * score >= target + best else 1

