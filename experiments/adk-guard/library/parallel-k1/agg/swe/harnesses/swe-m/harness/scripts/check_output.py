#!/usr/bin/env python3
"""Stop hook: block finishing until the fix and output/CHANGES.md exist and are usable.

Exit 2 (stderr goes to the agent) when a deterministic check fails; exit 0 otherwise.
Checks: output/CHANGES.md exists and is non-trivial; every non-test .py file compiles;
at least one non-test .py file was modified after the workspace was set up (mtime well
after the newest task file, e.g. ISSUE.md/tests); the existing tests pass (skipped if
pytest is missing). The mtime check is a heuristic, and the hook can block at most 3 times.
"""
import hashlib
import os
import pathlib
import py_compile
import subprocess
import sys

root = pathlib.Path.cwd()
problems = []

changes = root / "output" / "CHANGES.md"
if not changes.is_file() or len(changes.read_text(errors="ignore").strip()) < 20:
    problems.append("output/CHANGES.md is missing or nearly empty; write a short summary of what you "
                    "changed and why (after the fix is made and verified).")

SKIP = {"output", "tests", ".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}
src = [p for p in root.rglob("*.py")
       if not (set(p.relative_to(root).parts[:-1]) & SKIP) and p.name != "conftest.py"
       and not p.name.startswith("test_")]
for p in src:
    try:
        py_compile.compile(str(p), doraise=True)
    except py_compile.PyCompileError as e:
        problems.append(f"{p.relative_to(root)} does not compile: {e}")

digest = hashlib.md5(b"".join(p.read_bytes() for p in sorted(src))).hexdigest()
marker = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / ("stopsrc-" + hashlib.md5(str(root).encode()).hexdigest())
try:
    if marker.exists() and marker.read_text() == digest:
        problems.append("Your source files are byte-identical to the last time you tried to finish. "
                        "Re-writing the same code changes nothing: write DIFFERENT code that fixes the cause.")
    marker.write_text(digest)
except OSError:
    pass

refs = [p for p in [root / "ISSUE.md", *(root / "tests").rglob("*.py")] if p.is_file()]
if src and refs:
    base = max(p.stat().st_mtime for p in refs)
    if not any(p.stat().st_mtime > base + 2 for p in src):
        problems.append("No source file looks modified: you have not edited the code yet. Make the actual "
                        "edit (read the file, then write_file the full corrected source), re-run the "
                        "issue's example, then write output/CHANGES.md.")

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
