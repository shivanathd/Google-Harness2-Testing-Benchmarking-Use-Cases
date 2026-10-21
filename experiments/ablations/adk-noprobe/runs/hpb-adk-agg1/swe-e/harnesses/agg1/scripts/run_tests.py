#!/usr/bin/env python3
"""Run the workspace tests the way pytest would, without editing any test file.

Usage: python3 scripts/run_tests.py [tests_dir]   (default: tests)
Tries `python3 -m pytest -q`; if pytest is missing, imports every test_*.py with
src/ on sys.path (what tests/conftest.py does under pytest) and calls each test_*
function. Exit 0 = all passed, 1 = failures, 2 = nothing to run / usage error.
"""
import importlib.util
import pathlib
import subprocess
import sys
import traceback

tests = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "tests")
if not tests.is_dir():
    print(f"no such tests dir: {tests}")
    sys.exit(2)

r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(tests)],
                   capture_output=True, text=True)
if "No module named pytest" not in r.stderr:
    print(r.stdout + r.stderr)
    sys.exit(0 if r.returncode == 0 else 1)

sys.path.insert(0, str(pathlib.Path("src").resolve()))
ran = failed = 0
for f in sorted(tests.glob("test_*.py")):
    spec = importlib.util.spec_from_file_location(f.stem, f)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        traceback.print_exc()
        failed += 1
        continue
    for name in dir(mod):
        if name.startswith("test_") and callable(getattr(mod, name)):
            ran += 1
            try:
                getattr(mod, name)()
            except Exception:
                failed += 1
                print(f"FAIL {f.name}::{name}")
                traceback.print_exc()
print(f"ran={ran} failed={failed} (pytest unavailable; fallback runner)")
sys.exit(2 if ran == 0 else (1 if failed else 0))
