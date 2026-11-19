"""Run the saved student file once and record frames for the web page."""
import contextlib
import io
import json
from pathlib import Path
import sys

import farm
from levels import FILES, layout, stars


class Prints(io.StringIO):
    def write(self, value):
        available = 4000 - self.tell()
        if available > 0:
            super().write(value[:available])
        return len(value)


@contextlib.contextmanager
def limited(script):
    remaining = 20000
    def trace(frame, event, arg):
        nonlocal remaining
        if frame.f_code.co_filename != script:
            return None
        if event == "line":
            remaining -= 1
            if remaining <= 0:
                raise farm.FarmError("Your code took too long. Is a loop stuck?")
        return trace
    previous = sys.gettrace()
    sys.settrace(trace)
    try:
        yield
    finally:
        sys.settrace(previous)


def friendly(exc, script):
    line = getattr(exc, "lineno", None)
    trace = exc.__traceback__
    while trace:
        if trace.tb_frame.f_code.co_filename == script:
            line = trace.tb_lineno
        trace = trace.tb_next
    if isinstance(exc, IndentationError):
        tip = "Line up the spaces inside your function, loop, or if."
    elif isinstance(exc, SyntaxError):
        tip = "Check this line and the line above it. Look for a missing colon, quote, or parenthesis."
    elif isinstance(exc, NameError):
        tip = "Python could not find a name. Check its spelling and put crop names in quotes."
    elif isinstance(exc, KeyError):
        tip = f"Check your dictionary key {exc}. Each plot has \"crop\" and \"ready\"."
    elif isinstance(exc, IndexError):
        tip = "That plot number is outside the field. Try a loop over the field."
    elif isinstance(exc, TypeError):
        tip = "Check the arguments in your function call. " + str(exc)
    elif isinstance(exc, farm.FarmError):
        tip = str(exc)
    else:
        tip = f"Python stopped at {type(exc).__name__}. Check your last instruction."
    return {"line": line, "message": tip}


def run(level, field_name, path):
    script = str(path)
    scenario = layout(level, field_name)
    game = farm._start(level, scenario, script)
    prints = Prints()
    error = None
    source = ""
    try:
        source = path.read_text(encoding="utf-8")
        with contextlib.redirect_stdout(prints), contextlib.redirect_stderr(prints), limited(script):
            exec(compile(source, script, "exec"), {"__name__": "__main__", "__file__": script})
        if not game.finished:
            raise farm.FarmError("The run ended early. Keep the supplied day loop and main() call.")
    except (Exception, SystemExit) as exc:
        error = friendly(exc, script)
    score = game.basket if level < 2 else game.coins
    eligible = game.finished and not error and (not game.rules["timing_required"] or not game.wasted)
    earned = stars(score, scenario["target"], scenario["best"], eligible)
    return dict(level=level, field=field_name, filename=path.name, source=source,
                events=game.events, prints=prints.getvalue(), error=error, target=scenario["target"],
                stars=earned, best=scenario["best"], grow=farm._GROW,
                prices=farm._PRICES)


if __name__ == "__main__":
    level = int(sys.argv[1])
    print(json.dumps(run(level, sys.argv[2], Path(__file__).resolve().with_name(FILES[level]))))

