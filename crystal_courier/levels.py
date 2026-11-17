"""Supplied maps. Coordinates are (column, row), starting at zero."""


def make_level(key, title, width, height, sections, crystals, limit):
    grid = [["#"] * width for _ in range(height)]
    x, y = 1, 1
    grid[y][x] = "."
    for direction, count in sections:
        dx, dy = {"right": (1, 0), "down": (0, 1)}[direction]
        for _ in range(count):
            x, y = x + dx, y + dy
            grid[y][x] = "."
    return {"id": key, "title": title, "grid": ["".join(r) for r in grid],
            "start": [1, 1], "exit": [x, y], "crystals": crystals,
            "move_limit": limit}


LEVELS = {
    "tutorial": make_level("tutorial", "First delivery", 7, 5,
                           [("right", 3), ("down", 2)], [[4, 1]], 16),
    "challenge": make_level("challenge", "The crystal staircase", 14, 9,
                            [("right", 3), ("down", 2)] * 3 + [("right", 2)],
                            [[3, 1], [7, 4], [9, 5]], 30),
    "remix": make_level("remix", "New crystal positions", 14, 9,
                        [("right", 3), ("down", 2)] * 3 + [("right", 2)],
                        [[2, 1], [4, 3], [10, 7]], 30),
}
