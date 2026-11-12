"""Grader infrastructure. This file is not student work."""
import json
import runpy
import sys

namespace = runpy.run_path("defenders.py")
attack = namespace.get("attack")
if not callable(attack):
    raise SystemExit("Define attack(health, damages).")
for health, damages in json.loads(sys.argv[1]):
    result = attack(health, damages)
    if type(result) is not int:
        raise SystemExit("attack must return an integer, not print it.")
    print(result)
