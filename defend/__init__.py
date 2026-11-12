"""Defend the Base: assess the function, independently of the animation."""
import ast
import json
from pathlib import Path
import shlex

import check50


def _case(cases, expected):
    command = "python3 _runner.py " + shlex.quote(json.dumps(cases))
    process = check50.run(command)
    try:
        output = "".join(str(value) + "\n" for value in expected)
        process.stdout(r"\A" + output, output, timeout=3)
        process.stdout(check50.EOF, timeout=3).exit(0)
    finally:
        process.kill()


@check50.check()
def exists():
    """defenders.py exists"""
    check50.exists("defenders.py")
    check50.include("_runner.py")


@check50.check(exists)
def syntax():
    """defenders.py has valid Python syntax"""
    try:
        ast.parse(Path("defenders.py").read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError) as error:
        raise check50.Failure("Fix the Python syntax in defenders.py.", help=str(error))


@check50.check(syntax)
def two_towers():
    """attack(8, [2, 1]) returns 5"""
    _case([[8, [2, 1]]], [5])


@check50.check(syntax)
def one_tower():
    """a single tower fires once"""
    _case([[9, [4]]], [5])


@check50.check(syntax)
def three_towers():
    """all three towers contribute damage"""
    _case([[11, [1, 2, 1]]], [7])


@check50.check(syntax)
def exact_defeat():
    """exactly enough damage returns 0"""
    _case([[3, [2, 1]]], [0])


@check50.check(syntax)
def overkill():
    """extra damage returns 0, never negative health"""
    _case([[2, [2, 1]], [1, [8]]], [0, 0])


@check50.check(syntax)
def empty_defense():
    """an empty tower list leaves health unchanged"""
    _case([[7, []]], [7])


@check50.check(syntax)
def zero_damage():
    """zero-damage towers do not end the loop early"""
    _case([[9, [0, 2, 0, 3]], [5, [0, 0]]], [4, 5])


@check50.check(syntax)
def already_defeated():
    """an enemy starting at 0 stays at 0"""
    _case([[0, [2, 1]], [0, []]], [0, 0])


@check50.check(syntax)
def longer_list():
    """attack handles a longer, different list"""
    _case([[40, [1, 3, 2, 4, 1, 5, 2, 0]]], [22])


@check50.check(syntax)
def fresh_calls():
    """each call uses its own health and damages"""
    _case([[8, [2, 1]], [5, [2, 1]], [2, [2, 1]], [12, [4, 1]]], [5, 2, 0, 7])
