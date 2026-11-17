"""Supplied bridge: execute a saved file and return its actual movement records."""
import contextlib
import io
import json
from pathlib import Path
import sys
import traceback

import game
from levels import LEVELS


class ExecutionLimit(Exception):
    pass


class LimitedOutput(io.StringIO):
    def write(self, text):
        remaining = max(0, 8000 - self.tell())
        super().write(text[:remaining])
        return len(text)


def execute(script, level_id):
    script = Path(script).resolve()
    level = LEVELS[level_id]
    game._configure(level, script)
    source = script.read_text(encoding="utf-8")
    output = LimitedOutput()
    error = None
    count = 0

    def trace(frame, event, arg):
        nonlocal count
        if event == "line" and frame.f_code.co_filename == str(script):
            count += 1
            if count > 12000:
                raise ExecutionLimit("Loop stopped after 12,000 Python steps. Check what changes inside it.")
        return trace

    try:
        code = compile(source, str(script), "exec")
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            sys.settrace(trace)
            try:
                exec(code, {"__name__": "__main__", "__file__": str(script)})
            finally:
                sys.settrace(None)
    except BaseException as exc:
        sys.settrace(None)
        line = exc.lineno if isinstance(exc, SyntaxError) else None
        for frame in traceback.extract_tb(exc.__traceback__):
            if frame.filename == str(script):
                line = frame.lineno
        message = str(exc)
        if isinstance(exc, EOFError):
            message = "This visual runner has no input prompt. Use fixed arguments here; run controller.py in the terminal."
        if isinstance(exc, SystemExit):
            message = "The script exited early. Let your main() function finish normally."
        error = {"type": type(exc).__name__, "message": message, "line": line}
        if not game._state["events"][-1]["error"]:
            game._record(f'{error["type"]}: {message}', line, True)

    state = game._state
    won = not error and game.at_exit() and not state["remaining"]
    if error:
        message = error["message"]
    elif won:
        message = "Delivery complete! Every crystal reached the exit."
    elif game.at_exit():
        message = f'At the exit, but {len(state["remaining"])} crystal(s) still need collecting.'
    else:
        message = "Program finished. The robot still needs to reach the exit with every crystal."
    return {"level": level, "source": source, "filename": script.name,
            "events": state["events"], "won": won, "message": message,
            "error": error, "stdout": output.getvalue(), "moves": state["moves"]}


if __name__ == "__main__":
    print(json.dumps(execute(sys.argv[1], sys.argv[2])))
