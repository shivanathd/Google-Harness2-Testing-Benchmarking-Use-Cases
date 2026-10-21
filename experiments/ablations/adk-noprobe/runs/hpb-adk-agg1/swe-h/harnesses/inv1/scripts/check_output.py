#!/usr/bin/env python3
"""Stop-hook / manual completion check for an issue-resolution task.

Exit 0 = fine. Exit 2 = not done (reasons on stderr; the harness allows this at most 3 times).
Checks: output/CHANGES.md exists and is non-trivial and is not a copy of ISSUE.md; output/ holds
no copied ISSUE.md; every .py file compiles; at least one non-test .py file was modified after
ISSUE.md (a fix that edited no source is not a fix); every file path named in CHANGES.md exists;
the tests in tests/ pass.
"""
import pathlib
import py_compile
import re
import subprocess
import sys

problems = []
root = pathlib.Path(".")
out = root / "output"
changes = out / "CHANGES.md"
issue = root / "ISSUE.md"

text = ""
if not changes.is_file():
    problems.append("output/CHANGES.md is missing: write a short summary of the changes you actually made.")
else:
    text = changes.read_text(errors="replace")
    if len(text.strip()) < 40:
        problems.append("output/CHANGES.md is nearly empty.")
    if issue.is_file() and text.strip() == issue.read_text(errors="replace").strip():
        problems.append("output/CHANGES.md is a copy of ISSUE.md.")
if (out / "ISSUE.md").exists():
    problems.append("output/ISSUE.md is a stray copy of the task and is not a deliverable; do not rely on it. "
                    "Only output/CHANGES.md is requested; the fix belongs in the source files.")

py = [p for p in root.rglob("*.py")
      if not any(part.startswith(".") or part in ("output", "scripts", "__pycache__", "node_modules")
                 for part in p.parts)]
for f in py:
    try:
        py_compile.compile(str(f), doraise=True)
    except py_compile.PyCompileError as e:
        problems.append(f"{f} does not compile: {e}")

src = [p for p in py if "tests" not in p.parts and not p.name.startswith("test_") and p.name != "conftest.py"]
if issue.is_file() and src:
    base = issue.stat().st_mtime
    if not any(p.stat().st_mtime > base for p in src) and "no code change" not in text.lower():
        problems.append("No source file was modified after ISSUE.md. The fix must be written into the real "
                        "source files in place (not into output/). Edit them, re-read them, then update CHANGES.md.")

for m in set(re.findall(r"`([\w./-]+\.py)`", text)):
    if not (root / m).is_file() and not (out / m).is_file():
        problems.append(f"CHANGES.md names `{m}` but that file does not exist.")

if pathlib.Path("tests").is_dir():
    r = subprocess.run([sys.executable, str(pathlib.Path(__file__).parent / "run_tests.py")],
                       capture_output=True, text=True)
    if r.returncode == 1:
        problems.append("tests fail:\n" + (r.stdout + r.stderr)[-1500:])

if problems:
    print("Not done yet:\n- " + "\n- ".join(problems), file=sys.stderr)
    sys.exit(2)
