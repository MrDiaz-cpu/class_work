"""Behavior checks for Mr. Diaz's Week 2 Ticket Booth assignment."""

import ast
from pathlib import Path

import check50


@check50.check()
def exists():
    """tickets.py exists"""
    check50.exists("tickets.py")


@check50.check(exists)
def syntax():
    """tickets.py has valid Python syntax"""
    try:
        ast.parse(Path("tickets.py").read_text(encoding="utf-8"))
    except SyntaxError as error:
        raise check50.Failure(
            f"Syntax error on line {error.lineno}: {error.msg}",
            help="Check indentation, colons, parentheses, and quotation marks.",
        ) from error


def _check_session(inputs):
    """Require a fresh prompt for every attempt and exact final ticket lines."""
    process = check50.run("python3 tickets.py")
    try:
        for value in inputs:
            # Anchoring prevents output before a prompt from being swallowed.
            process.stdout(r"\ATickets: ", "Tickets: ", timeout=3)
            process.stdin(str(value), prompt=False)

        count = inputs[-1]
        expected = "".join(
            f"Ticket {number}: {'GOLD' if number % 2 else 'BLUE'}\n"
            for number in range(1, count + 1)
        )
        # Ticket lines contain no regex metacharacters. Anchor the first line,
        # then require EOF so extra tickets or debug messages cannot pass.
        process.stdout(r"\A" + expected, expected, timeout=3)
        process.stdout(check50.EOF, timeout=3).exit(0)
    finally:
        process.kill()


@check50.check(syntax)
def one_ticket():
    """1 prints only Ticket 1: GOLD"""
    _check_session([1])


@check50.check(syntax)
def two_tickets():
    """2 prints GOLD then BLUE, numbered 1 and 2"""
    _check_session([2])


@check50.check(syntax)
def four_tickets():
    """4 prints exactly four numbered tickets with alternating colors"""
    _check_session([4])


@check50.check(syntax)
def five_tickets():
    """5 prints exactly five tickets and ends with GOLD"""
    _check_session([5])


@check50.check(syntax)
def ten_tickets():
    """10 is accepted and prints exactly ten tickets"""
    _check_session([10])


@check50.check(syntax)
def rejects_zero():
    """0 is rejected; entering 3 next prints three tickets"""
    _check_session([0, 3])


@check50.check(syntax)
def rejects_negative():
    """-2 is rejected; entering 2 next prints two tickets"""
    _check_session([-2, 2])


@check50.check(syntax)
def rejects_above_ten():
    """11 is rejected; entering 2 next prints two tickets"""
    _check_session([11, 2])


@check50.check(syntax)
def repeated_invalid():
    """keeps asking after -2, 0, and 12; accepts 1 afterward"""
    _check_session([-2, 0, 12, 1])
