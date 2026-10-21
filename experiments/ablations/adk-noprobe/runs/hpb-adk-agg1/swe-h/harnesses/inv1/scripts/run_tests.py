#!/usr/bin/env python3
"""Run the workspace tests without editing any test file.

Usage: python3 scripts/run_tests.py [tests_dir]   (default: tests)
Tries `python3 -m pytest -q` from the workspace root; if pytest is missing, imports every
test_*.py with the workspace root and src/ on sys.path and calls each test_* function
(a `tmp_path` argument is supplied; tests needing other fixtures are reported as skipped).
Exit 0 = all passed, 1 = failures, 2 = nothing ran / usage error.
"""
import importlib.util
import inspect
import pathlib
import subprocess
import sys
import tempfile
import traceback

tests = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "tests")
if not tests.is_dir():
    print(f"no such tests dir: {tests}")
    sys.exit(2)

r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(tests)], capture_output=True, text=True)
if "No module named pytest" not in r.stderr:
    print(r.stdout + r.stderr)
    sys.exit(0 if r.returncode == 0 else 1)

for p in (pathlib.Path("src").resolve(), pathlib.Path(".").resolve()):
    sys.path.insert(0, str(p))
ran = failed = skipped = 0
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
        fn = getattr(mod, name)
        if not (name.startswith("test_") and callable(fn)):
            continue
        params = list(inspect.signature(fn).parameters)
        if any(p != "tmp_path" for p in params):
            skipped += 1
            print(f"SKIP {f.name}::{name} (needs fixtures {params})")
            continue
        ran += 1
        try:
            if params:
                with tempfile.TemporaryDirectory() as d:
                    fn(pathlib.Path(d))
            else:
                fn()
        except Exception:
            failed += 1
            print(f"FAIL {f.name}::{name}")
            traceback.print_exc()
print(f"ran={ran} failed={failed} skipped={skipped} (pytest unavailable; fallback runner)")
sys.exit(2 if ran == 0 else (1 if failed else 0))
