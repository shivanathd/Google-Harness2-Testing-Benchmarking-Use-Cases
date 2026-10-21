#!/usr/bin/env python3
"""Stop hook: block finishing until output/ copies exist, match src/, and tests pass.

Exit 2 (stderr shown to agent) when a problem is found; exit 0 otherwise.
Checks only deterministic facts: output/*.py present, compiles, identical to the
src/ file of the same name, and (if pytest and tests/ exist) the tests pass.
"""
import filecmp
import pathlib
import py_compile
import subprocess
import sys

root = pathlib.Path.cwd()
problems = []
outs = sorted((root / "output").glob("*.py")) if (root / "output").is_dir() else []
if not outs:
    problems.append("output/ has no .py deliverable; cp the final source file there.")
for out in outs:
    try:
        py_compile.compile(str(out), doraise=True)
    except py_compile.PyCompileError as e:
        problems.append(f"{out} does not compile: {e}")
    src = root / "src" / out.name
    if src.exists() and not filecmp.cmp(src, out, shallow=False):
        problems.append(f"{out} differs from {src}; re-copy the final source.")
if (root / "tests").is_dir():
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "tests"],
                           capture_output=True, text=True, timeout=90)
        if r.returncode not in (0, 5) and "No module named pytest" not in r.stderr:
            problems.append("tests fail:\n" + (r.stdout + r.stderr)[-1500:])
    except Exception:
        pass
if problems:
    print("Cannot finish yet:\n" + "\n".join(problems), file=sys.stderr)
    sys.exit(2)
