"""Supplied game commands. Students import these; no editing required."""
import inspect


class GameError(Exception):
    """A legal Python instruction that cannot be completed in the game."""


_state = None
_script = None


def _configure(level, script):
    global _state, _script
    _script = str(script)
    _state = {"level": level, "position": list(level["start"]),
              "remaining": [list(p) for p in level["crystals"]],
              "moves": 0, "events": [], "actions": 0}
    _record("Ready", None)


def _ready():
    if _state is None:
        raise RuntimeError("Start the visual game with: python play.py . "
                           "Then choose a level and click Run saved Python in the browser.")


def _line():
    frame = inspect.currentframe()
    try:
        while frame:
            if frame.f_code.co_filename == _script:
                return frame.f_lineno
            frame = frame.f_back
    finally:
        del frame
    return None


def _record(action, line, error=False):
    _state["events"].append({"action": action, "line": line,
        "position": list(_state["position"]), "remaining": [list(p) for p in _state["remaining"]],
        "moves": _state["moves"], "error": error})


def _fail(message):
    _record(message, _line(), True)
    raise GameError(message)


def _direction(direction):
    directions = {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}
    if not isinstance(direction, str) or direction not in directions:
        raise ValueError('Use "right", "left", "up", or "down".')
    return directions[direction]


def _destination(direction):
    _ready()
    dx, dy = _direction(direction)
    x, y = _state["position"]
    return [x + dx, y + dy]


def _floor(position):
    x, y = position
    grid = _state["level"]["grid"]
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != "#"


def _action():
    _ready()
    _state["actions"] += 1
    if _state["actions"] > 120:
        _fail("Too many actions. Check the stopping condition of your loop.")


def move(direction):
    """Move exactly one square in an absolute screen direction."""
    _action()
    target = _destination(direction)
    if _state["moves"] >= _state["level"]["move_limit"]:
        _fail("Move limit reached. Plan a shorter route and run again.")
    if not _floor(target):
        _fail(f'Wall ahead: move("{direction}") cannot enter that square.')
    _state["position"] = target
    _state["moves"] += 1
    _record(f'move("{direction}")', _line())


def on_crystal():
    """Return True if an uncollected crystal is under the robot."""
    _ready()
    return _state["position"] in _state["remaining"]


def collect():
    """Pick up the crystal under the robot; fail on an empty square."""
    _action()
    if not on_crystal():
        _fail("No crystal here. Check on_crystal() before collecting.")
    _state["remaining"].remove(_state["position"])
    _record("collect()", _line())


def can_move(direction):
    """Return True if the adjacent square is floor; does not move."""
    return _floor(_destination(direction))


def at_exit():
    """Return True at the exit, whether or not all crystals were collected."""
    _ready()
    return _state["position"] == _state["level"]["exit"]
