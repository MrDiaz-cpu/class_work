"""Crystal Courier checks for the student's mission.py."""
import ast
from pathlib import Path

import check50


def _case(name):
    process = check50.run("python3 _grade.py " + name)
    try:
        process.stdout(r"\APASS\r?\n", "PASS\n", timeout=3)
        process.stdout(check50.EOF, timeout=3).exit(0)
    finally:
        process.kill()


@check50.check()
def exists():
    """mission.py exists"""
    check50.exists("mission.py")
    check50.include("_grade.py", "game.py", "levels.py", "runner.py")


@check50.check(exists)
def syntax():
    """mission.py has valid Python syntax"""
    try:
        ast.parse(Path("mission.py").read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError) as error:
        raise check50.Failure("Fix the Python syntax in mission.py.", help=str(error))


@check50.check(syntax)
def functions():
    """mission.py defines walk and main"""
    tree = ast.parse(Path("mission.py").read_text(encoding="utf-8"))
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    for name in ("walk", "main"):
        if name not in names:
            raise check50.Failure(f"Define the function {name} in mission.py.")


@check50.check(functions)
def right():
    """walk moves right for the requested number of steps"""
    _case("right")


@check50.check(functions)
def left():
    """walk uses its direction argument to move left"""
    _case("left")


@check50.check(functions)
def up():
    """walk uses its direction argument to move up"""
    _case("up")


@check50.check(functions)
def down():
    """walk uses its direction argument to move down"""
    _case("down")


@check50.check(functions)
def zero():
    """walk takes no actions when steps is zero"""
    _case("zero")


@check50.check(functions)
def crystals():
    """walk collects crystals after each step, including the final step"""
    _case("crystals")


@check50.check(functions)
def repeated():
    """walk works on repeated calls with different arguments"""
    _case("repeated")


@check50.check(syntax)
def challenge():
    """the saved program collects all crystals and reaches the Challenge exit"""
    _case("challenge")


@check50.check(syntax)
def remix():
    """the same saved program completes Remix with new crystal positions"""
    _case("remix")
