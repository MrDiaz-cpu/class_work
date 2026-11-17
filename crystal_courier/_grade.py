"""Trusted check50 harness. Only mission.py is supplied by the student."""
import ast
import contextlib
import io
from pathlib import Path
import sys

import game
from runner import execute


def load_functions():
    path = Path("mission.py").resolve()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    # Unit checks call walk directly. The level checks execute the original file.
    tree.body = [node for node in tree.body if not (
        isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name) and node.value.func.id == "main")]
    namespace = {"__name__": "mission", "__file__": str(path)}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(tree, str(path), "exec"), namespace)
    for name in ("walk", "main"):
        if not callable(namespace.get(name)):
            raise AssertionError(f"Define a function named {name}.")
    return namespace


def probe(direction, steps, start, crystals=(), namespace=None):
    level = {"id": "probe", "title": "Check50 practice room",
             "grid": ["########", "#......#", "#......#", "#......#", "#......#", "########"],
             "start": start, "exit": [6, 4], "crystals": [list(p) for p in crystals], "move_limit": 30}
    game._configure(level, Path("mission.py").resolve())
    namespace = namespace if namespace is not None else load_functions()
    game._configure(level, Path("mission.py").resolve())
    dx, dy = {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}[direction]
    position = list(start)
    remaining = [list(p) for p in crystals]
    expected = []
    for _ in range(steps):
        position = [position[0] + dx, position[1] + dy]
        expected.append((f'move("{direction}")', list(position)))
        if position in remaining:
            remaining.remove(position)
            expected.append(("collect()", list(position)))
    with contextlib.redirect_stdout(io.StringIO()):
        namespace["walk"](direction, steps)
    actual = [(e["action"], e["position"]) for e in game._state["events"][1:]]
    if actual != expected or game._state["remaining"] != remaining:
        raise AssertionError(f"walk({direction!r}, {steps}) should take exactly {steps} steps in that direction "
                             "and collect any crystal immediately after reaching its square. "
                             f"Expected actions: {expected}. Actual actions: {actual}.")
    return namespace


def run(case):
    if case in ("challenge", "remix"):
        result = execute("mission.py", case)
        if not result["won"]:
            raise AssertionError(result["message"])
    elif case == "right":
        probe("right", 3, [1, 1])
    elif case == "left":
        probe("left", 2, [5, 2])
    elif case == "up":
        probe("up", 2, [3, 3])
    elif case == "down":
        probe("down", 2, [1, 1])
    elif case == "zero":
        probe("right", 0, [1, 1], [[1, 1]])
    elif case == "crystals":
        probe("right", 4, [1, 1], [[2, 1], [4, 1], [5, 1]])
    elif case == "repeated":
        namespace = probe("right", 1, [1, 1], [[2, 1]])
        probe("down", 3, [2, 1], [[2, 2], [2, 4]], namespace)
        probe("left", 2, [5, 2], (), namespace)
    else:
        raise ValueError("Unknown check.")


if __name__ == "__main__":
    try:
        run(sys.argv[1])
    except BaseException as error:
        print(f"FAIL: {type(error).__name__}: {error}")
        sys.exit(1)
    print("PASS")
