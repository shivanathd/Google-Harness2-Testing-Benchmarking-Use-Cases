[ACTION] Bash {"command": "ls -la && cat ISSUE.md && ls -R tests output 2>/dev/null | head -50", "description": "List workspace and read the issue"}
[OBSERVATION]
Exit code 1
ls: ..: Operation not permitted
ls: fts_read: Operation not permitted
total 16
drwxr-xr-x@ 7 me  staff  224 Oct 19 02:11 .
-rw-r--r--@ 1 me  staff  172 Oct 19 02:11 CLAUDE.md
-rw-r--r--@ 1 me  staff  825 Oct 19 01:13 ISSUE.md
drwxr-xr-x@ 2 me  staff   64 Oct 19 01:13 output
drwxr-xr-x@ 6 me  staff  192 Oct 19 01:13 stock
drwxr-xr-x@ 3 me  staff   96 Oct 19 01:13 tests
[ACTION] Bash {"command": "cat ISSUE.md; echo ---; find stock tests output -not -path '*/.git*' | head -100", "description": "Read the issue and list stock, tests, output"}
[OBSERVATION]
# Inventory CLI: three fixes for the next release

1. `stock report` crashes when the stock file does not exist yet or is empty. Treat both
   as an empty inventory (`store.load` returns `{}`).
2. `remove` lets quantities go below zero and silently creates unknown SKUs. `ops.remove`
   must raise ValueError instead and leave the data unchanged. `ops.add` must likewise
   raise ValueError for a quantity that is not positive. In the CLI, any such error prints
   `error: <message>` to stderr, returns exit status 1 and leaves the file unchanged.
3. Feature: `stock report --low N` lists only SKUs with quantity < N, sorted by quantity
   ascending, then by SKU. The plain `stock report` output (`SKU<TAB>QTY` lines sorted by
   SKU) must not change -- other tools parse it.

`stock.cli.main(argv)` returns the exit status.
---
stock
tests
output
tests/test_cli.py
stock/store.py
stock/__init__.py
stock/ops.py
stock/cli.py
[ACTION] Bash {"command": "for f in stock/*.py tests/test_cli.py; do echo \"=== $f\"; cat -n \"$f\"; done", "description": "Print source and test files with line numbers"}
[OBSERVATION]
=== stock/__init__.py
=== stock/cli.py
     1	import argparse
     2	
     3	from . import ops, store
     4	
     5	
     6	def main(argv=None):
     7	    p = argparse.ArgumentParser(prog="stock")
     8	    p.add_argument("--file", default="stock.json")
     9	    sub = p.add_subparsers(dest="cmd", required=True)
    10	    a = sub.add_parser("add")
    11	    a.add_argument("sku")
    12	    a.add_argument("qty", type=int)
    13	    r = sub.add_parser("remove")
    14	    r.add_argument("sku")
    15	    r.add_argument("qty", type=int)
    16	    sub.add_parser("report")
    17	    args = p.parse_args(argv)
    18	    data = store.load(args.file)
    19	    if args.cmd == "add":
    20	        ops.add(data, args.sku, args.qty)
    21	    elif args.cmd == "remove":
    22	        ops.remove(data, args.sku, args.qty)
    23	    else:
    24	        for sku in sorted(data):
    25	            print(f"{sku}\t{data[sku]}")
    26	        return 0
    27	    store.save(args.file, data)
    28	    return 0
=== stock/ops.py
     1	def add(data, sku, qty):
     2	    data[sku] = data.get(sku, 0) + qty
     3	    return data
     4	
     5	
     6	def remove(data, sku, qty):
     7	    data[sku] = data.get(sku, 0) - qty
     8	    return data
=== stock/store.py
     1	import json
     2	
     3	
     4	def load(path):
     5	    with open(path) as f:
     6	        return json.load(f)
     7	
     8	
     9	def save(path, data):
    10	    with open(path, "w") as f:
    11	        json.dump(data, f, indent=2, sort_keys=True)
=== tests/test_cli.py
     1	import json
     2	
     3	from stock.cli import main
     4	
     5	
     6	def test_add_then_file(tmp_path):
     7	    f = tmp_path / "s.json"
     8	    f.write_text("{}")
     9	    assert main(["--file", str(f), "add", "bolt", "3"]) == 0
    10	    assert json.loads(f.read_text()) == {"bolt": 3}
[ASSISTANT] Three fixes are clear from the issue. I'll read the files through the Read tool so I can edit them.
[ACTION] Read {"file_path": "./stock/store.py"}
[OBSERVATION]
1	import json
2	
3	
4	def load(path):
5	    with open(path) as f:
6	        return json.load(f)
7	
8	
9	def save(path, data):
10	    with open(path, "w") as f:
11	        json.dump(data, f, indent=2, sort_keys=True)
12	
[ACTION] Read {"file_path": "./stock/ops.py"}
[OBSERVATION]
1	def add(data, sku, qty):
2	    data[sku] = data.get(sku, 0) + qty
3	    return data
4	
5	
6	def remove(data, sku, qty):
7	    data[sku] = data.get(sku, 0) - qty
8	    return data
9	
[ACTION] Read {"file_path": "./stock/cli.py"}
[OBSERVATION]
1	import argparse
2	
3	from . import ops, store
4	
5	
6	def main(argv=None):
7	    p = argparse.ArgumentParser(prog="stock")
8	    p.add_argument("--file", default="stock.json")
9	    sub = p.add_subparsers(dest="cmd", required=True)
10	    a = sub.add_parser("add")
11	    a.add_argument("sku")
12	    a.add_argument("qty", type=int)
13	    r = sub.add_parser("remove")
14	    r.add_argument("sku")
15	    r.add_argument("qty", type=int)
16	    sub.add_parser("report")
17	    args = p.parse_args(argv)
18	    data = store.load(args.file)
19	    if args.cmd == "add":
20	        ops.add(data, args.sku, args.qty)
21	    elif args.cmd == "remove":
22	        ops.remove(data, args.sku, args.qty)
23	    else:
24	        for sku in sorted(data):
25	            print(f"{sku}\t{data[sku]}")
26	        return 0
27	    store.save(args.file, data)
28	    return 0
29	
[ACTION] Read {"file_path": "./tests/test_cli.py"}
[OBSERVATION]
1	import json
2	
3	from stock.cli import main
4	
5	
6	def test_add_then_file(tmp_path):
7	    f = tmp_path / "s.json"
8	    f.write_text("{}")
9	    assert main(["--file", str(f), "add", "bolt", "3"]) == 0
10	    assert json.loads(f.read_text()) == {"bolt": 3}
11	
[ASSISTANT] Plan, with verification for each step:
1. `store.load` returns `{}` for a missing or blank file → verify with tests.
2. `ops.add`/`ops.remove` raise `ValueError` before mutating → verify with tests.
3. CLI prints `error: ...` to stderr and returns 1 without saving → verify with tests.
4. `report --low N` filters and sorts; plain report is unchanged → verify with tests.

Starting with the store.
[ACTION] Edit {"replace_all": false, "file_path": "./stock/store.py", "old_string": "import json\n\n\ndef load(path):\n    with open(path) as f:\n        return json.load(f)", "new_string": "import json\nimport os\n\n\ndef load(path):\n    if not os.path.exists(path):\n        return {}\n    with open(path) as f:\n        text = f.read()\n    if not text.strip():\n        return {}\n    return json.loads(text)"}
[OBSERVATION]
The file ./stock/store.py has been updated successfully. (file state is current in your context — no need to Read it back)
[ACTION] Edit {"replace_all": false, "file_path": "./stock/ops.py", "old_string": "def add(data, sku, qty):\n    data[sku] = data.get(sku, 0) + qty\n    return data\n\n\ndef remove(data, sku, qty):\n    data[sku] = data.get(sku, 0) - qty\n    return data", "new_string": "def add(data, sku, qty):\n    if qty <= 0:\n        raise ValueError(f\"quantity must be positive, got {qty}\")\n    data[sku] = data.get(sku, 0) + qty\n    return data\n\n\ndef remove(data, sku, qty):\n    if qty <= 0:\n        raise ValueError(f\"quantity must be positive, got {qty}\")\n    if sku not in data:\n        raise ValueError(f\"unknown SKU: {sku}\")\n    left = data[sku] - qty\n    if left < 0:\n        raise ValueError(f\"cannot remove {qty} of {sku}: only {data[sku]} in stock\")\n    data[sku] = left\n    return data"}
[OBSERVATION]
The file ./stock/ops.py has been updated successfully. (file state is current in your context — no need to Read it back)
[ACTION] Edit {"replace_all": false, "file_path": "./stock/cli.py", "old_string": "import argparse\n\nfrom . import ops, store", "new_string": "import argparse\nimport sys\n\nfrom . import ops, store"}
[OBSERVATION]
The file ./stock/cli.py has been updated successfully. (file state is current in your context — no need to Read it back)
[ASSISTANT] Now the CLI body: the report option, the error handling, and the low-stock filter.
[ACTION] Edit {"replace_all": false, "file_path": "./stock/cli.py", "old_string": "    sub.add_parser(\"report\")\n    args = p.parse_args(argv)\n    data = store.load(args.file)\n    if args.cmd == \"add\":\n        ops.add(data, args.sku, args.qty)\n    elif args.cmd == \"remove\":\n        ops.remove(data, args.sku, args.qty)\n    else:\n        for sku in sorted(data):\n            print(f\"{sku}\\t{data[sku]}\")\n        return 0\n    store.save(args.file, data)\n    return 0", "new_string": "    rep = sub.add_parser(\"report\")\n    rep.add_argument(\"--low\", type=int)\n    args = p.parse_args(argv)\n    data = store.load(args.file)\n    try:\n        if args.cmd == \"add\":\n            ops.add(data, args.sku, args.qty)\n        elif args.cmd == \"remove\":\n            ops.remove(data, args.sku, args.qty)\n        else:\n            if args.low is None:\n                rows = sorted(data.items())\n            else:\n                rows = sorted(\n                    (kv for kv in data.items() if kv[1] < args.low),\n                    key=lambda kv: (kv[1], kv[0]),\n                )\n            for sku, qty in rows:\n                print(f\"{sku}\\t{qty}\")\n            return 0\n    except ValueError as e:\n        print(f\"error: {e}\", file=sys.stderr)\n        return 1\n    store.save(args.file, data)\n    return 0"}
[OBSERVATION]
The file ./stock/cli.py has been updated successfully. (file state is current in your context — no need to Read it back)
[ASSISTANT] Next, regression tests for each behavior in the issue, appended to the existing test file.
[ACTION] Edit {"replace_all": false, "file_path": "./tests/test_cli.py", "old_string": "import json\n\nfrom stock.cli import main\n\n\ndef test_add_then_file(tmp_path):\n    f = tmp_path / \"s.json\"\n    f.write_text(\"{}\")\n    assert main([\"--file\", str(f), \"add\", \"bolt\", \"3\"]) == 0\n    assert json.loads(f.read_text()) == {\"bolt\": 3}", "new_string": "import json\n\nimport pytest\n\nfrom stock import ops\nfrom stock.cli import main\n\n\ndef test_add_then_file(tmp_path):\n    f = tmp_path / \"s.json\"\n    f.write_text(\"{}\")\n    assert main([\"--file\", str(f), \"add\", \"bolt\", \"3\"]) == 0\n    assert json.loads(f.read_text()) == {\"bolt\": 3}\n\n\ndef test_report_missing_or_empty_file(tmp_path, capsys):\n    missing = tmp_path / \"none.json\"\n    assert main([\"--file\", str(missing), \"report\"]) == 0\n    empty = tmp_path / \"empty.json\"\n    empty.write_text(\"\")\n    assert main([\"--file\", str(empty), \"report\"]) == 0\n    assert capsys.readouterr().out == \"\"\n\n\ndef test_ops_reject_non_positive_and_leave_data_unchanged():\n    data = {\"bolt\": 2}\n    with pytest.raises(ValueError):\n        ops.add(data, \"bolt\", 0)\n    with pytest.raises(ValueError):\n        ops.remove(data, \"bolt\", 0)\n    with pytest.raises(ValueError):\n        ops.remove(data, \"bolt\", 3)\n    with pytest.raises(ValueError):\n        ops.remove(data, \"nut\", 1)\n    assert data == {\"bolt\": 2}
[OBSERVATION]
The file ./tests/test_cli.py has been updated successfully. (file state is current in your context — no need to Read it back)
[ACTION] Bash {"command": "(python -m pytest tests -q 2>&1 || python -m pytest tests -q -p no:cacheprovider 2>&1) | tail -30", "description": "Run the test suite with pytest"}
[OBSERVATION]
==================================== ERRORS ====================================
________________________ ERROR collecting test session _________________________
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/pathlib/_abc.py:482: in is_file
    return S_ISREG(self.stat(follow_symlinks=follow_symlinks).st_mode)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/pathlib/_local.py:515: in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   PermissionError: [Errno 1] Operation not permitted: '<runs>/exec/hpb-cc-agg1/swe-h/agg1'
=========================== short test summary info ============================
ERROR  - PermissionError: [Errno 1] Operation not permitted: '/Users/me...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.07s

==================================== ERRORS ====================================
________________________ ERROR collecting test session _________________________
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/pathlib/_abc.py:482: in is_file
    return S_ISREG(self.stat(follow_symlinks=follow_symlinks).st_mode)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/pathlib/_local.py:515: in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   PermissionError: [Errno 1] Operation not permitted: '<runs>/exec/hpb-cc-agg1/swe-h/agg1'
=========================== short test summary info ============================
ERROR  - PermissionError: [Errno 1] Operation not permitted: '/Users/me...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.10s
[ASSISTANT] Pytest fails while walking parent directories for config (a sandbox permission on the parent folder), before any test runs. I'll point it at an explicit empty config and rootdir so it doesn't walk upward.
[ACTION] Bash {"command": "python -m pytest -c /dev/null --rootdir . tests -q -p no:cacheprovider 2>&1 | tail -30", "description": "Run pytest with explicit config and rootdir"}
[OBSERVATION]
ERROR: found no collectors for ./tests


==================================== ERRORS ====================================
________________________ ERROR collecting test session _________________________
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/site-packages/pluggy/_caller.py:197: in __call__
    return self._hookexec(
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/site-packages/pluggy/_manager.py:183: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/site-packages/_pytest/main.py:467: in pytest_ignore_collect
    if collection_path.is_dir():
       ^^^^^^^^^^^^^^^^^^^^^^^^
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/pathlib/_abc.py:465: in is_dir
    return S_ISDIR(self.stat(follow_symlinks=follow_symlinks).st_mode)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/pathlib/_local.py:515: in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   PermissionError: [Errno 1] Operation not permitted: '/Users/me/.aws'
=========================== short test summary info ============================
ERROR ::Users::me - PermissionError: [Errno 1] Operation not perm...
1 error in 0.08s
[ASSISTANT] Pytest is still reaching outside the workspace (`~/.aws`), which the sandbox blocks. I'll try limiting its config search with `--confcutdir`.
[ACTION] Bash {"command": "python -m pytest -c /dev/null --rootdir . --confcutdir . tests -q -p no:cacheprovider 2>&1 | tail -15", "description": "Run pytest with confcutdir limited to workspace"}
[OBSERVATION]
==================================== ERRORS ====================================
________________________ ERROR collecting test session _________________________
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/pathlib/_abc.py:482: in is_file
    return S_ISREG(self.stat(follow_symlinks=follow_symlinks).st_mode)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/pathlib/_local.py:515: in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   PermissionError: [Errno 1] Operation not permitted: '<runs>/exec/hpb-cc-agg1/swe-h/agg1'
=========================== short test summary info ============================
ERROR  - PermissionError: [Errno 1] Operation not permitted: '/Users/me...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.30s
[ASSISTANT] Pytest's collection is blocked by the sandbox in every mode. I'll run the test functions with plain Python from a runner in `/tmp`, outside the workspace, supplying `tmp_path` and `capsys` myself.
[ACTION] Bash {"command": "mkdir -p /tmp/stock_runner && cat > /tmp/stock_runner/run.py <<'PY'\nimport contextlib, importlib.util, inspect, io, pathlib, sys, tempfile, traceback\n\nwork = pathlib.Path(sys.argv[1])\nsys.path.insert(0, str(work))\nspec = importlib.util.spec_from_file_location(\"test_cli\", work / \"tests\" / \"test_cli.py\")\nmod = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(mod)\n\n\nclass Capsys:\n    def __init__(self):\n        self.out, self.err = io.StringIO(), io.StringIO()\n\n    def readouterr(self):\n        r = (self.out.getvalue(), self.err.getvalue())\n        self.out.seek(0); self.out.truncate(); self.err.seek(0); self.err.truncate()\n        return type(\"R\", (), {\"out\": r[0], \"err\": r[1]})\n\n\npassed = failed = 0\nfor name, fn in inspect.getmembers(mod, inspect.isfunction):\n    if not name.startswith(\"test_\"):\n        continue\n    kwargs = {}\n    params = inspect.signature(fn).parameters\n    with tempfile.TemporaryDirectory() as d:\n        if \"tmp_path\" in params:\n            kwargs[\"tmp_path\"] = pathlib.Path(d)\n        cap = Capsys()\n        if \"capsys\" in params:\n            kwargs[\"capsys\"] = cap\n        try:\n            with contextlib.redirect_stdout(cap.out), contextlib.redirect_stderr(cap.err):\n                fn(**kwargs)\n            passed += 1\n            print(\"PASS\", name)\n        except Exception:\n            failed += 1\n            print(\"FAIL\", name)\n            traceback.print_exc()\np
[OBSERVATION]
Exit code 1
Traceback (most recent call last):
  File "/private/tmp/stock_runner/run.py", line 7, in <module>
    spec.loader.exec_module(mod)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "./tests/test_cli.py", line 3, in <module>
    import pytest
  File "/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/site-packages/pytest/__init__.py", line 8, in <module>
    from _pytest._code import ExceptionInfo
  File "/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/site-packages/_pytest/_code/__init__.py", line 5, in <module>
    from .code import Code
  File "/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/site-packages/_pytest/_code/code.py", line 41, in <module>
    from _pytest._io import TerminalWriter
  File "/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/site-packages/_pytest/_io/__init__.py", line 3, in <module>
    from .terminalwriter import get_terminal_width
  File "/Users/me/.local/share/mise/installs/python/3.13.16/lib/python3.13/site-packages/_pytest/_io/terminalwriter.py", line 13, in <module>
    import pygments
ModuleNotFoundError: No module named 'pygments'
[ASSISTANT] The `-I` flag hid the user's site-packages, so pytest's dependencies went missing. The runner lives in its own directory with no shadowing modules, so I'll drop `-I`.
[ACTION] Bash {"command": "cd /tmp/stock_runner && python run.py .", "description": "Run test functions with plain Python runner"}
[OBSERVATION]
PASS test_add_then_file
PASS test_cli_remove_error_exits_1_and_keeps_file
PASS test_cli_remove_unknown_sku_does_not_create_it
PASS test_ops_reject_non_positive_and_leave_data_unchanged
PASS test_report_low_sorted_by_qty_then_sku
PASS test_report_missing_or_empty_file
PASS test_report_plain_sorted_by_sku
7 passed, 0 failed
Shell cwd was reset to .
[ASSISTANT] All 7 tests pass. Now I'll write the changes summary and clean up the temporary runner.
[ACTION] Write {"file_path": "./output/CHANGES.md", "content": "# Changes\n\n1. **`stock report` on missing/empty file** (`stock/store.py`): `load` returns `{}` when the file does not exist or contains only whitespace.\n\n2. **Validation in `remove`/`add`** (`stock/ops.py`):\n   - `add` raises `ValueError` for a quantity <= 0.\n   - `remove` raises `ValueError` for a quantity <= 0, an unknown SKU, or a result below zero. Checks run before any mutation, so `data` is unchanged on error.\n\n3. **CLI error handling** (`stock/cli.py`): `ValueError` from `ops` prints `error: <message>` to stderr, returns 1, and skips `store.save`, so the file is unchanged.\n\n4. **`stock report --low N`** (`stock/cli.py`): lists SKUs with qty < N, sorted by qty then SKU. Plain `report` output is unchanged (SKU-sorted, `SKU<TAB>QTY`).\n\nTests: added cases to `tests/test_cli.py` covering each item above. All 7 tests pass.\nNote: `python -m pytest` could not run in this sandbox (pytest fails walking parent directories outside the workspace with a permission error). The tests were run with a plain-Python runner that calls the same test functions.\n"}
[OBSERVATION]
File created successfully at: ./output/CHANGES.md (file state is current in your context — no need to Read it back)
[ACTION] Bash {"command": "rm -rf /tmp/stock_runner", "description": "Remove temporary test runner directory"}
[OBSERVATION]
(Bash completed with no output)
[ASSISTANT] All three fixes from ISSUE.md are in, and the 7 tests pass. I could not run `python -m pytest` here: pytest fails while scanning parent directories outside the workspace, and the sandbox blocks that. I ran the test functions with a plain-Python runner instead, so pytest itself has not been run.

**Changes**
- **`stock/store.py`**: `load` returns `{}` when the file is missing or blank.
- **`stock/ops.py`**: `add` raises `ValueError` for a quantity ≤ 0. `remove` raises `ValueError` for a quantity ≤ 0, an unknown SKU, or a result below zero. All checks run before any mutation, so the data is unchanged on error.
- **`stock/cli.py`**:
  - A `ValueError` prints `error: <message>` to stderr, returns 1, and skips the save.
  - `report --low N` filters to qty < N and sorts by qty, then SKU.
  - Plain `report` output is unchanged.
- **`tests/test_cli.py`**: I added regression tests for each item. This goes slightly beyond "fix the issue," so say if you'd rather drop them.
- **`output/CHANGES.md`**: summary of the above.

**Choices I made**
- A whitespace-only file is treated as empty, not as a JSON error.
- Removing a SKU down to exactly 0 keeps the key with value 0, as before.
- `--low` takes an integer and does no further validation.