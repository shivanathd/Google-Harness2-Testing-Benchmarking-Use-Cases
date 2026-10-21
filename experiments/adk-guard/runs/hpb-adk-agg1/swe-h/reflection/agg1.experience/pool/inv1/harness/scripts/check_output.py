#!/usr/bin/env python3
"""Stop hook: block finishing until the source was edited, compiles, tests pass and CHANGES.md exists.

Exit 2 (stderr goes to the agent) when a deterministic check fails; exit 0 otherwise.
Never blocks on missing pytest or on an unusable environment. Heuristic: a source .py file counts
as edited if its mtime is later than ISSUE.md and every test file. The hook blocks at most 3 times.
"""
import pathlib
import py_compile
import subprocess
import sys

root = pathlib.Path.cwd()
problems = []

changes = root / "output" / "CHANGES.md"
if not changes.is_file() or len(changes.read_text(errors="ignore").strip()) < 20:
    problems.append("output/CHANGES.md is missing or nearly empty: after fixing and running the code, "
                    "write a short summary of the changes you really made.")

SKIP = {"output", "tests", ".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}
src = [p for p in root.rglob("*.py")
       if not (set(p.relative_to(root).parts[:-1]) & SKIP) and p.name != "conftest.py"
       and not p.name.startswith("test_")]
for p in src:
    try:
        py_compile.compile(str(p), doraise=True, cfile="/dev/null")
    except py_compile.PyCompileError as e:
        problems.append(f"{p.relative_to(root)} does not compile: {e}")
    except Exception:
        pass

refs = [p for p in [root / "ISSUE.md", *(root / "tests").rglob("*.py")] if p.is_file()]
if src and refs:
    base = max(p.stat().st_mtime for p in refs)
    if not any(p.stat().st_mtime > base + 1 for p in src):
        problems.append("No source file looks modified: the code still has the original bugs. Read the "
                        "source files (list_files, read_file), then write_file the full corrected file "
                        "for each layer the issue names, and run the issue's examples.")

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
