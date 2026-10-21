#!/usr/bin/env python3
"""Run the workspace tests from the workspace root.

Usage: python3 scripts/run_tests.py [pytest args...]
Tries pytest (honours tests/conftest.py); if pytest is not installed, falls back
to unittest discovery with src/ on PYTHONPATH. Exit code is the test runner's.
"""
import os
import subprocess
import sys

root = os.getcwd()
env = dict(os.environ)
env["PYTHONPATH"] = os.pathsep.join(
    [p for p in (os.path.join(root, "src"), root, env.get("PYTHONPATH", "")) if p]
)
args = sys.argv[1:]

probe = subprocess.run([sys.executable, "-c", "import pytest"], capture_output=True)
if probe.returncode == 0:
    cmd = [sys.executable, "-m", "pytest", "-q", *(args or ["tests"])]
else:
    print("pytest not available; falling back to unittest discovery", file=sys.stderr)
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
sys.exit(subprocess.run(cmd, cwd=root, env=env).returncode)
