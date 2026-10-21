#!/usr/bin/env python3
"""Pre-finish check for issue-resolution tasks. Run from the workspace root.

Checks: a non-test .py source file was edited after the workspace was set up; edited
files compile and have no undefined names (e.g. a missing import); output/CHANGES.md
exists and names every edited file; output/ISSUE.md is not a copy of the issue; existing
tests pass (skipped if pytest is unavailable). Exit 2 + stderr = problems, 0 = ok.
"""
import ast
import builtins
import os
import subprocess
import sys

problems = []
SKIP = {"output", "node_modules", "venv", "site-packages"}


def walk():
    for root, dirs, files in os.walk("."):
        # hidden dirs (.local, .cache, .git, .pytest_cache ...) hold pip installs and caches
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".") and d != "__pycache__"]
        for f in files:
            yield os.path.join(root, f)


allf = list(walk())
pys = [p for p in allf if p.endswith(".py") and os.sep + "scripts" + os.sep not in p]
others = [p for p in allf if not p.endswith((".py", ".pyc"))]

# Baseline = newest mtime among files the agent normally leaves alone (issue, docs).
base = max([os.path.getmtime(p) for p in others] or [0])
is_test = lambda p: "tests" in p.split(os.sep) or os.path.basename(p).startswith("test_")
edited = [p for p in pys if os.path.getmtime(p) > base + 1]
src_edited = [p for p in edited if not is_test(p)]
if not src_edited:
    problems.append("No non-test .py source file has been edited. The issue must be fixed in the source "
                    "files themselves: read them and edit them with write_file (output/ISSUE.md copies "
                    "do not count).")


def undefined_names(path):
    try:
        tree = ast.parse(open(path, errors="replace").read(), path)
    except SyntaxError as e:
        return ["syntax error line %s: %s" % (e.lineno, e.msg)]
    bound = set(dir(builtins)) | {"__file__", "__name__"}
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(n.name)
        elif isinstance(n, ast.arg):
            bound.add(n.arg)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                bound.add((a.asname or a.name).split(".")[0])
        elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            bound.add(n.id)
        elif isinstance(n, ast.ExceptHandler) and n.name:
            bound.add(n.name)
    return sorted({"undefined name '%s' (missing import?)" % n.id for n in ast.walk(tree)
                   if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id not in bound})


for p in edited:
    for msg in undefined_names(p):
        problems.append("%s: %s" % (p, msg))

if os.path.exists(os.path.join("output", "ISSUE.md")):
    problems.append("output/ISSUE.md is a copy of the issue; delete it (output/ holds only CHANGES.md).")

cp = os.path.join("output", "CHANGES.md")
if not os.path.isfile(cp) or not open(cp, errors="replace").read().strip():
    problems.append("output/CHANGES.md is missing or empty: write a short summary of the edits you made.")
else:
    text = open(cp, errors="replace").read()
    missing = [os.path.basename(p) for p in edited
               if os.path.basename(p) not in text and os.path.splitext(os.path.basename(p))[0] not in text]
    if missing:
        problems.append("output/CHANGES.md does not mention edited file(s): " + ", ".join(missing))

if os.path.isdir("tests"):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-x", "-q"],
                           capture_output=True, text=True, timeout=120)
        out = r.stdout + r.stderr
        if "No module named pytest" in out or ("ModuleNotFoundError" in out and "_pytest" in out
                                               and "collected" not in out):
            pass
        elif r.returncode not in (0, 5):
            problems.append("Tests fail (python -m pytest tests); fix the code or the test:\n" + out[-1500:])
    except Exception as e:
        problems.append("Could not run tests: %r (run them yourself)" % e)

if problems:
    sys.stderr.write("Do not finish yet. Act now with tool calls (write_file / run_command), "
                     "do not just describe what you will do:\n- " + "\n- ".join(problems) + "\n")
    sys.exit(2)
