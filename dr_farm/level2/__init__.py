"""Dr. Farm · Level 2 checks."""
import ast
from pathlib import Path

import check50


STUDENT = "level2.py"


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
    """level2.py exists"""
    check50.exists(STUDENT)
    check50.include("_grade.py", "_secret.py", "farm.py", "runner.py", "levels.py")


@check50.check(exists)
def syntax():
    """level2.py has valid Python syntax"""
    try:
        ast.parse(Path(STUDENT).read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError) as error:
        raise check50.Failure("Fix the syntax in " + STUDENT, help=str(error))


@check50.check(syntax)
def functions():
    """level2.py defines tend and work_day"""
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
def plant():
    """tend plants on empty soil when seeds remain"""
    _case("plant", "Check for empty soil and look in the seed bag.")


@check50.check(functions)
def last_seed():
    """tend plants the only crop left in the bag"""
    _case("last_seed", "Skip a crop when its seed count is zero.")


@check50.check(functions)
def empty_bag():
    """tend leaves an empty plot alone when the bag is empty"""
    _case("empty_bag", "Check the seed count before calling plant.")


@check50.check(functions)
def once():
    """tend takes at most one action per call"""
    _case("once", "Once you choose an action, stop working on this plot.")


@check50.check(functions)
def visit():
    """work_day tends every plot exactly once"""
    _case("visit", "Loop over the field, including a field with zero plots.")


@check50.check(functions)
def challenge():
    """Challenge reaches 15 coins"""
    _case("challenge", "Try both fields in the browser. Step through the log to see what your code does.")


@check50.check(functions)
def remix():
    """Remix reaches 20 coins"""
    _case("remix", "Try both fields in the browser. Step through the log to see what your code does.")


@check50.check(functions)
def secret():
    """the Secret field reaches its target"""
    _case("secret", "Try both fields in the browser. Step through the log to see what your code does.")

