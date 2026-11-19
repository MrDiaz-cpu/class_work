"""Dr. Farm · Level 1 checks."""
import ast
from pathlib import Path

import check50


STUDENT = "level1.py"


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
    """level1.py exists"""
    check50.exists(STUDENT)
    check50.include("_grade.py", "_secret.py", "farm.py", "runner.py", "levels.py")


@check50.check(exists)
def syntax():
    """level1.py has valid Python syntax"""
    try:
        ast.parse(Path(STUDENT).read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError) as error:
        raise check50.Failure("Fix the syntax in " + STUDENT, help=str(error))


@check50.check(syntax)
def functions():
    """level1.py defines tend and work_day"""
    tree = ast.parse(Path(STUDENT).read_text(encoding="utf-8"))
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name in ("tend", "work_day"):
        if name not in names:
            raise check50.Failure(f"Define {name} in " + STUDENT, help="Keep the function names in the starter.")


@check50.check(functions)
def water():
    """tend waters each kind of growing crop"""
    _case("water", "Water a crop that still needs to grow.")


@check50.check(functions)
def harvest():
    """tend harvests each kind of ready crop"""
    _case("harvest", "Read the ready value in this plot.")


@check50.check(functions)
def once():
    """tend takes at most one action per call"""
    _case("once", "Once you choose an action, stop working on this plot.")


@check50.check(functions)
def visit():
    """work_day tends every plot exactly once"""
    _case("visit", "Loop over the field, including a field with zero plots.")


@check50.check(functions)
def given():
    """work_day uses the field it is given"""
    _case("given", "Use the function argument. The field can change size and order.")


@check50.check(functions)
def challenge():
    """Challenge reaches 10 harvests"""
    _case("challenge", "Try both fields in the browser. Step through the log to see what your code does.")


@check50.check(functions)
def remix():
    """Remix reaches 14 harvests"""
    _case("remix", "Try both fields in the browser. Step through the log to see what your code does.")


@check50.check(functions)
def secret():
    """the Secret field reaches its target"""
    _case("secret", "Try both fields in the browser. Step through the log to see what your code does.")

