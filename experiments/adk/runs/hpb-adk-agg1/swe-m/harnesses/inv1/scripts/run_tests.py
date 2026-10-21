#!/usr/bin/env python3
"""Run the workspace tests from the workspace root.

Usage: python3 scripts/run_tests.py [pytest args...]
Uses pytest if importable. Otherwise imports every tests/test_*.py and calls each
top-level test_* function (plain asserts). Exit code 0 only if all pass; exit 2 if
no tests were found.
"""
import glob
import importlib.util
import os
import subprocess
import sys
import traceback

root = os.getcwd()
for p in (root, os.path.join(root, "src")):
    if os.path.isdir(p):
        sys.path.insert(0, p)
env = dict(os.environ)
env["PYTHONPATH"] = os.pathsep.join(p for p in (root, os.path.join(root, "src"), env.get("PYTHONPATH", "")) if p)

if subprocess.run([sys.executable, "-c", "import pytest"], capture_output=True).returncode == 0:
    sys.exit(subprocess.run([sys.executable, "-m", "pytest", "-q", *(sys.argv[1:] or ["tests"])], cwd=root, env=env).returncode)

print("pytest not available; running test_* functions directly", file=sys.stderr)
ran = failed = 0
for path in sorted(glob.glob(os.path.join(root, "tests", "test_*.py"))):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        traceback.print_exc()
        failed += 1
        continue
    for name in sorted(dir(mod)):
        fn = getattr(mod, name)
        if name.startswith("test_") and callable(fn):
            ran += 1
            try:
                fn()
                print("PASS", path, name)
            except Exception:
                failed += 1
                print("FAIL", path, name)
                traceback.print_exc()
print(f"{ran} ran, {failed} failed")
sys.exit(2 if ran == 0 and not failed else (1 if failed else 0))
