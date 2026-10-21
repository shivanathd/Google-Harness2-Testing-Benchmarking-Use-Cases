#!/usr/bin/env python3
"""Stop-hook / manual check that the deliverable exists and is usable.

Passes (exit 0) when output/ holds at least one .py file, each is byte-identical to
its src/ counterpart, compiles, and the tests in tests/ pass. Otherwise prints the
reason to stderr and exits 2 (the harness blocks finishing, at most 3 times).
"""
import pathlib
import py_compile
import subprocess
import sys

problems = []
out = pathlib.Path("output")
files = sorted(out.glob("*.py")) if out.is_dir() else []
if not files:
    problems.append("output/ has no .py deliverable. Copy the fixed src file to output/<same name> "
                    "(run_command: cp src/<name>.py output/<name>.py) after the tests pass.")
for f in files:
    src = pathlib.Path("src") / f.name
    if not src.is_file():
        problems.append(f"{f} has no counterpart src/{f.name}.")
    elif src.read_bytes() != f.read_bytes():
        problems.append(f"{f} differs from {src}: re-copy after your last edit.")
    try:
        py_compile.compile(str(f), doraise=True)
    except py_compile.PyCompileError as e:
        problems.append(f"{f} does not compile: {e}")

here = pathlib.Path(__file__).parent
if pathlib.Path("tests").is_dir():
    r = subprocess.run([sys.executable, str(here / "run_tests.py")], capture_output=True, text=True)
    if r.returncode == 1:
        problems.append("tests fail:\n" + (r.stdout + r.stderr)[-1500:])

if problems:
    print("Not done yet:\n- " + "\n- ".join(problems), file=sys.stderr)
    sys.exit(2)
