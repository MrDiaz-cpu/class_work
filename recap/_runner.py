"""Grader helper. Students do not download, edit, or submit this file."""
import json
import sys

import recap

if not callable(getattr(recap, "show_results", None)):
    raise SystemExit("Keep a function named show_results(scores) in recap.py.")

for scores in json.loads(sys.argv[1]):
    recap.show_results(scores)
