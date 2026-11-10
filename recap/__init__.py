"""Game Score Recap: checks for the published student specification."""
import ast
import json
from pathlib import Path
import shlex

import check50


def _expected(scores):
    lines = []
    for number, score in enumerate(scores, start=1):
        outcome = "WIN" if score >= 10 else "LOSS"
        lines.append(f"Round {number}: {score} points - {outcome}")
    lines.append(f"Wins: {sum(score >= 10 for score in scores)}")
    return "\n".join(lines) + "\n"


def _run_exact(command, expected):
    process = check50.run(command)
    try:
        if expected:
            # The expected text contains no regex metacharacters. Anchor the start
            # so debug output or a second recap cannot be silently skipped.
            process.stdout(r"\A" + expected, expected, timeout=3)
        process.stdout(check50.EOF, timeout=3).exit(0)
    finally:
        process.kill()


def _case(*lists):
    argument = shlex.quote(json.dumps(lists))
    _run_exact("python3 _runner.py " + argument,
               "".join(_expected(scores) for scores in lists))


@check50.check()
def exists():
    """recap.py exists"""
    check50.exists("recap.py")
    check50.include("_runner.py")


@check50.check(exists)
def syntax():
    """recap.py has valid Python syntax"""
    try:
        ast.parse(Path("recap.py").read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError) as error:
        raise check50.Failure("Fix the Python syntax in recap.py.", help=str(error))


@check50.check(syntax)
def function_ready():
    """show_results exists and the supplied main guard is preserved"""
    _case()


@check50.check(function_ready)
def sample():
    """running recap.py prints the four-round sample and Wins: 2"""
    _run_exact("python3 recap.py", _expected([8, 15, 4, 12]))


@check50.check(function_ready)
def boundary():
    """9 is a loss; 10 and 11 are wins"""
    _case([9, 10, 11])


@check50.check(function_ready)
def no_wins():
    """[0, 9, 3] prints every loss and Wins: 0"""
    _case([0, 9, 3])


@check50.check(function_ready)
def all_wins():
    """[10, 11, 20] counts all three wins"""
    _case([10, 11, 20])


@check50.check(function_ready)
def repeated_scores():
    """repeated scores are separate rounds and wins"""
    _case([12, 12, 4])


@check50.check(function_ready)
def one_round():
    """a one-round recap starts at Round 1"""
    _case([7])


@check50.check(function_ready)
def ten_rounds():
    """round numbers continue through Round 10"""
    _case([2, 15, 0, 10, 8, 22, 9, 1, 11, 4])


@check50.check(function_ready)
def different_list():
    """show_results uses the supplied scores, not the sample list"""
    _case([99, 2, 17, 6, 10])


@check50.check(function_ready)
def fresh_counters():
    """each call starts a new recap with fresh counters"""
    _case([15, 10], [3, 4], [10])
