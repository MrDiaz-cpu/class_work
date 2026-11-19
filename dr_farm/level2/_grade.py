"""Trusted scenarios. build.py copies this file beside each check suite."""
import ast
import contextlib
import os
from pathlib import Path
import signal
import sys

import farm
from levels import layout
from runner import friendly, limited
from _secret import LEVEL, SECRET

PATH = Path(f"level{LEVEL}.py").resolve()
CROPS = tuple(farm._GROW)


def require(ok, tip):
    if not ok:
        raise AssertionError(tip)


def load_student():
    tree = ast.parse(PATH.read_text(encoding="utf-8"), str(PATH))
    last = tree.body[-1] if tree.body else None
    if isinstance(last, ast.Expr) and isinstance(last.value, ast.Call):
        func = last.value.func
        if isinstance(func, ast.Name) and func.id == "main":
            tree.body.pop()
    ns = {"__name__": "student", "__file__": str(PATH)}
    exec(compile(tree, str(PATH), "exec"), ns)
    return ns


def tend(ns, days):
    args = (days,) if LEVEL == 3 else ()
    ns["tend"](farm.field[0], *args)


def probe(ns, crop, stage, expected, bag=(), days=9, day=1, exactly=True):
    counts = {c: 1 for c in bag}
    game = farm._start(LEVEL, {"plots": [(crop, stage)], "seeds": counts})
    game.day = day
    tend(ns, days)
    actions = game.events[1:]
    if expected is None:
        require(not actions, "Leave this empty plot alone. No seed can be planted here today.")
        return
    require(actions, f"Call {expected} on this plot.")
    first = actions[0]
    require(first["action"] == expected and first["ok"],
            f"This plot needs {expected}. " + (first["message"] or "Check your if and else branches."))
    if expected == "plant":
        require(first["crop"] in bag, "Plant a crop that has a seed left.")
    if exactly:
        require(len(actions) == 1, "Stop after choosing one action for this plot.")
    return first["crop"]


def visits(ns, size, subset, days=6):
    game = farm._start(LEVEL, {"plots": [("corn", 0)] * size})
    given = farm.field[1::2][::-1] if subset else farm.field.copy()
    calls = []
    def observe(plot, *arguments):
        calls.append((id(plot), arguments))
    ns["tend"] = observe
    args = (days,) if LEVEL == 3 else ()
    ns["work_day"](given, *args)
    require(sorted(calls) == sorted((id(p), args) for p in given) and len(game.events) == 1,
            "Call tend once per plot in the field you receive." +
            (" Pass the same days_left to each call." if LEVEL == 3 else ""))


def run_field(ns, name):
    data = SECRET if name == "secret" else layout(LEVEL, name)
    game = farm._start(LEVEL, data)
    visited = set()
    for day in range(1, 11):
        args = (10-day,) if LEVEL == 3 else ()
        start = len(game.events)
        ns["work_day"](farm.field, *args)
        require(game.day == day and not game.finished, "Let the supplied day loop call sleep().")
        visited.update(e["plot"] for e in game.events[start:] if e["plot"] is not None)
        farm.sleep()
    score = game.basket if LEVEL == 1 else game.coins
    require(score >= data["target"], f"You earned {score}. The goal is {data['target']}.")
    if LEVEL == 1:
        require(len(visited) == len(data["plots"]), "Visit every plot, including the last ones.")
    if LEVEL == 3:
        require(game.wasted == 0, f"{game.wasted} seeds ran out of time. Leave a day to harvest.")


def run(case):
    ns = load_student()
    if case in ("challenge", "remix", "secret"):
        run_field(ns, case)
    elif case in ("water", "harvest", "care"):
        for c in CROPS:
            if case != "harvest":
                probe(ns, c, farm._GROW[c]-1, "water", exactly=False)
            if case != "water":
                probe(ns, c, farm._GROW[c], "harvest", exactly=False)
    elif case == "once":
        probe(ns, "corn", 0, "water")
        probe(ns, "pumpkin", 5, "harvest")
        if LEVEL >= 2:
            probe(ns, "empty", 0, "plant", CROPS)
    elif case == "visit":
        if LEVEL == 1:
            tree = ast.parse(PATH.read_text(encoding="utf-8"))
            fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "work_day")
            require(any(isinstance(node, ast.For) for node in ast.walk(fn)), "Use a for loop in work_day to visit the plots.")
        for size in (1, 5, 0):
            visits(ns, size, False)
    elif case == "given":
        visits(ns, 9, True)
    elif case == "plant":
        probe(ns, "empty", 0, "plant", CROPS, exactly=False)
    elif case == "last_seed":
        for c in CROPS:
            probe(ns, "empty", 0, "plant", (c,), exactly=False)
    elif case == "empty_bag":
        probe(ns, "empty", 0, None)
    elif case == "radish3":
        probe(ns, "empty", 0, "plant", ("radish",), days=3)
    elif case == "radish2":
        probe(ns, "empty", 0, None, ("radish",), days=2)
    elif case == "mixed":
        chosen = probe(ns, "empty", 0, "plant", ("pumpkin", "radish"), days=3)
        require(chosen == "radish", "Try the next seed when the first one needs too many days.")
    elif case == "pumpkin3":
        probe(ns, "empty", 0, None, ("pumpkin",), days=3)
    elif case == "boundary":
        for c in ("corn", "pumpkin"):
            n = farm._GROW[c]
            probe(ns, "empty", 0, "plant", (c,), days=n+1)
            probe(ns, "empty", 0, None, (c,), days=n)
    elif case == "argument":
        for current in (1, 5, 9):
            for days in (2, 3, 0, 8):
                probe(ns, "empty", 0, "plant" if days > 2 else None, ("radish",), days, current)
    elif case == "forward":
        for days in (0, 3, 8):
            visits(ns, 5, True, days)
    else:
        raise ValueError("Unknown check case.")


def timeout(*_):
    raise farm.FarmError("Your code took too long. Is a loop stuck?")


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(3)
    try:
        with open(os.devnull, "w") as quiet, contextlib.redirect_stdout(quiet), contextlib.redirect_stderr(quiet), limited(str(PATH)):
            run(sys.argv[1])
    except BaseException as exc:
        msg = str(exc) if isinstance(exc, AssertionError) else friendly(exc, str(PATH))["message"]
        print("Try again. " + msg)
        sys.exit(1)
    finally:
        signal.alarm(0)
    print("PASS")

