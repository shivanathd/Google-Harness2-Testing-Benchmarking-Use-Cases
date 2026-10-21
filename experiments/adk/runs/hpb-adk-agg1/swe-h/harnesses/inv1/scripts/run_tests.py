#!/usr/bin/env python3
"""Run the workspace tests from the workspace root.

Usage: python3 scripts/run_tests.py [pytest args...]
Uses pytest if installed (honours conftest.py). Otherwise runs a plain-python
fallback: imports tests/test_*.py with the root and src/ on sys.path, calls each
test_* function, and supplies a `tmp_path` pathlib fixture. Tests needing other
fixtures are reported as UNSUPPORTED (not passed). Exit code 0 only if all ran and passed.
"""
import importlib.util
import inspect
import os
import pathlib
import subprocess
import sys
import tempfile
import traceback

root = os.getcwd()
env = dict(os.environ)
env["PYTHONPATH"] = os.pathsep.join(
    [p for p in (os.path.join(root, "src"), root, env.get("PYTHONPATH", "")) if p]
)
args = sys.argv[1:]

probe = subprocess.run([sys.executable, "-c", "import pytest"], capture_output=True)
if probe.returncode == 0:
    sys.exit(subprocess.run([sys.executable, "-m", "pytest", "-q", *(args or ["tests"])],
                            cwd=root, env=env).returncode)

print("pytest not available; using plain-python fallback", file=sys.stderr)
sys.path[:0] = [root, os.path.join(root, "src")]
passed = failed = unsupported = 0
for path in sorted(pathlib.Path(root, "tests").glob("test_*.py")):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception:
        print(f"ERROR importing {path.name}"); traceback.print_exc(); failed += 1; continue
    for name, fn in sorted(vars(mod).items()):
        if not (name.startswith("test_") and callable(fn)):
            continue
        params = list(inspect.signature(fn).parameters)
        if any(p != "tmp_path" for p in params):
            print(f"UNSUPPORTED {path.name}::{name} (fixtures: {params})"); unsupported += 1; continue
        try:
            with tempfile.TemporaryDirectory() as d:
                fn(*([pathlib.Path(d)] if params else []))
            print(f"PASS {path.name}::{name}"); passed += 1
        except Exception:
            print(f"FAIL {path.name}::{name}"); traceback.print_exc(); failed += 1
print(f"{passed} passed, {failed} failed, {unsupported} unsupported")
sys.exit(1 if failed or unsupported else 0)
