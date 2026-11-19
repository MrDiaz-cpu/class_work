"""The supplied farm engine. Your code chooses actions. The engine keeps score."""
import sys
from pathlib import Path

from levels import FILES, RULES, layout

DAYS = 10
_GROW = {"radish": 2, "carrot": 3, "corn": 4, "pumpkin": 5}
_PRICES = {"radish": 1, "carrot": 2, "corn": 4, "pumpkin": 7}
grow_days = dict(_GROW)
prices = dict(_PRICES)
plot = {}
field = []
seeds = {}
_farm = None


class FarmError(Exception):
    """A mistake that stops the student's program, with a classroom-friendly message."""


class Farm:
    def __init__(self, level, layout, script=None):
        self.level = level
        self.rules = dict(RULES[level], **{k: layout[k] for k in RULES[level] if k in layout})
        self.actions_today = 0
        self.script = script
        self.day = 1
        self.basket = self.coins = self.wasted = 0
        self.finished = False
        self.bag = {name: layout.get("seeds", {}).get(name, 0) for name in _GROW}
        self.plots = [dict(crop=crop, stage=stage, wet=False, worked=False, wasted=False)
                      for crop, stage in layout["plots"]]
        self.views = [{} for p in self.plots]
        if level == 0 and self.views:
            self.views[0] = plot
        self.events = []
        self.refresh()
        self.record("start")

    def refresh(self):
        field[:] = self.views
        for view, plot in zip(self.views, self.plots):
            crop = plot["crop"]
            view.clear()
            view.update(crop=crop, ready=crop != "empty" and plot["stage"] == _GROW[crop])
        for snapshot, original in [(seeds, self.bag), (grow_days, _GROW), (prices, _PRICES)]:
            # Updating values preserves the student's active dictionary iterator.
            for extra in snapshot.keys() - original.keys():
                del snapshot[extra]
            snapshot.update(original)

    def state(self):
        return {"day": self.day, "days_left": DAYS - self.day, "finished": self.finished,
                "basket": self.basket, "coins": self.coins, "wasted": self.wasted,
                "seeds": self.bag.copy(), "plots": [p.copy() for p in self.plots]}

    def record(self, action, index=None, message="", ok=True, crop=None, day=None):
        line = None
        frame = sys._getframe(1)
        while frame:
            if frame.f_code.co_filename == self.script:
                line = frame.f_lineno
                break
            frame = frame.f_back
        self.events.append(dict(action=action, plot=index, line=line, message=message,
                                ok=ok, crop=crop, day=day or self.day, state=self.state()))

    def act(self, action, view, seed=None):
        if self.finished:
            raise FarmError("Day 10 is over. Run saved Python to start a fresh farm.")
        self.actions_today += 1
        if self.actions_today > 1000:
            raise FarmError("Your code took too long. Is a loop stuck?")
        index = next((i for i, handle in enumerate(self.views) if handle is view), None)
        if index is None:
            if isinstance(view, list):
                raise FarmError(f"{action}() needs one plot from the field, not the whole field.")
            raise FarmError(f"{action}() needs one plot from the field. Pass the plot from your loop.")
        p = self.plots[index]
        crop = p["crop"]
        ready = crop != "empty" and p["stage"] == _GROW[crop]
        message = ""
        if p["worked"]:
            message = "Already worked here today!"
        elif action == "harvest":
            if not ready:
                message = "Not ready!"
            elif self.rules["auto_replant"]:
                self.basket += 1
                p.update(stage=0, wasted=False)
            else:
                self.coins += _PRICES[crop]
                p.update(crop="empty", stage=0, wasted=False)
        elif action == "water":
            if crop == "empty":
                message = "Nothing planted!"
            elif ready:
                message = "Already ripe!"
            else:
                p["wet"] = True
        elif action == "plant":
            if not self.rules["planting_enabled"]:
                message = "Plant seeds in Level 2 or Level 3."
            elif crop != "empty":
                message = "Already planted!"
            elif not isinstance(seed, str) or seed not in _GROW:
                message = f"There's no seed called '{seed}'."
            elif self.bag[seed] == 0:
                message = "No seeds!"
            else:
                self.bag[seed] -= 1
                late = _GROW[seed] >= DAYS - self.day
                p.update(crop=seed, stage=0, wasted=late)
                self.wasted += int(late)
        p["worked"] = True
        ok = not message
        if action == "plant" and ok and p["wasted"] and self.rules["timing_required"]:
            message = "Won't ripen in time!"
        self.refresh()
        self.record(action, index, message, ok, seed if action == "plant" else crop)

    def sleep(self):
        if self.finished:
            raise FarmError("The farm has ten days. Check your day loop.")
        ended = self.day
        self.actions_today = 0
        for plot in self.plots:
            if plot["wet"]:
                plot["stage"] += 1
            plot.update(wet=False, worked=False)
        self.finished = self.day == DAYS
        if not self.finished:
            self.day += 1
        self.refresh()
        self.record("sleep", day=ended)


def _start(level, layout, script=None):
    global _farm
    _farm = Farm(level, layout, script)
    return _farm


def _current():
    if _farm is None:
        raise FarmError("Start the game with python play.py, then click Run saved Python.")
    return _farm


def water(plot):
    _current().act("water", plot)


def harvest(plot):
    _current().act("harvest", plot)


def plant(plot, crop):
    _current().act("plant", plot, crop)


def sleep():
    _current().sleep()



# A direct run uses the same Challenge field as the browser.
if Path(sys.argv[0]).name in FILES:
    import atexit
    _level = FILES.index(Path(sys.argv[0]).name)
    _setting = layout(_level, "challenge")
    _local = _start(_level, _setting, str(Path(sys.argv[0]).resolve()))

    def _summary():
        unit = "harvested" if _local.rules["auto_replant"] else "coins"
        score = _local.basket if _local.rules["auto_replant"] else _local.coins
        print(f"Day {_local.day} of 10 · {score} {unit} / {_setting['target']} · {_local.wasted} wasted seeds")

    import signal

    def _timeout(*unused):
        raise FarmError("Your code took too long. Is a loop stuck?")

    def _explain(kind, error, traceback):
        from runner import friendly
        details = friendly(error, _local.script)
        location = f"Line {details['line']} · " if details["line"] else ""
        print(location + details["message"], file=sys.stderr)

    sys.excepthook = _explain
    atexit.register(_summary)
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, _timeout)
        signal.alarm(5)
        atexit.register(signal.alarm, 0)
