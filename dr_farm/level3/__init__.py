"""Dr. Farm · Level 3 checks."""
import ast
from pathlib import Path

import check50


STUDENT = "level3.py"


def _case(name, hint):
    process = check50.run("python3 _grade.py " + name)
    try:
        result = process.stdout(timeout=5)
        if result != "PASS\n":
            raise check50.Failure(result.strip() or "Your code took too long. Is a loop stuck?", help=hint)
        if process.exitcode != 0:
            raise check50.Failure("Python stopped early.", help=hint)
    finally:
        process.kill()


@check50.check()
def exists():
    """level3.py exists"""
    check50.exists(STUDENT)
    check50.include("_grade.py", "_secret.py", "farm.py", "runner.py", "levels.py")


@check50.check(exists)
def syntax():
    """level3.py has valid Python syntax"""
    try:
        ast.parse(Path(STUDENT).read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError) as error:
        raise check50.Failure("Fix the syntax in " + STUDENT, help=str(error))


@check50.check(syntax)
def functions():
    """level3.py defines tend and work_day"""
    tree = ast.parse(Path(STUDENT).read_text(encoding="utf-8"))
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name in ("tend", "work_day"):
        if name not in names:
            raise check50.Failure(f"Define {name} in " + STUDENT, help="Keep the function names in the starter.")


@check50.check(functions)
def care():
    """tend waters growing crops and harvests ready crops"""
    _case("care", "Check what the planted crop needs today.")


@check50.check(functions)
def radish3():
    """tend plants radish with exactly 3 days left"""
    _case("radish3", "Count two watering days and one harvest day.")


@check50.check(functions)
def radish2():
    """tend plants nothing with 2 days left and only radish seeds"""
    _case("radish2", "A radish needs two waterings and a separate harvest.")


@check50.check(functions)
def mixed():
    """tend picks radish when a pumpkin would take too long"""
    _case("mixed", "Keep looking if a seed needs too many days.")


@check50.check(functions)
def pumpkin3():
    """tend leaves the pumpkin seed in the bag with 3 days left"""
    _case("pumpkin3", "Compare the watering days with the days left.")


@check50.check(functions)
def boundary():
    """tend checks the last safe day for corn and pumpkin"""
    _case("boundary", "Save a separate day for harvest.")


@check50.check(functions)
def argument():
    """tend uses the days_left argument it is given"""
    _case("argument", "Read the argument each time the function runs.")


@check50.check(functions)
def forward():
    """work_day passes days_left to tend for each plot"""
    _case("forward", "Pass both the plot and the days left.")


@check50.check(functions)
def challenge():
    """Challenge reaches 15 coins with zero wasted seeds"""
    _case("challenge", "Try both fields in the browser. Step through the log to see what your code does.")


@check50.check(functions)
def remix():
    """Remix reaches 20 coins with zero wasted seeds"""
    _case("remix", "Try both fields in the browser. Step through the log to see what your code does.")


@check50.check(functions)
def secret():
    """the Secret field reaches its target with zero wasted seeds"""
    _case("secret", "Try both fields in the browser. Step through the log to see what your code does.")

