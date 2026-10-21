Evidence: one rollout (base1). It failed in these ways:
- It never fixed `parse_duration`. Its first `write_file` rewrote `src/durations.py` unchanged, with the `[hm]` regex still missing `s`.
- It ran `python3 tests/test_durations.py` directly. That failed with `ModuleNotFoundError` because `tests/conftest.py` only puts `src/` on `sys.path` under pytest.
- It treated that error as a bug. It overwrote `tests/test_durations.py` with a one-line import, three times, which destroyed the existing test. It also added `src/__init__.py`.
- It never wrote `output/durations.py`, which the task requires.

Changes:
1. New skill `skills/fix-python-bug/SKILL.md`.
   - It treats the docstring as the controlling spec ("fully meets its docstring") and the existing tests as a floor.
   - It says to run tests with pytest from the workspace root, and explains the direct-run `ModuleNotFoundError` as a harness mistake. This targets the direct-run failure above.
   - It forbids overwriting or truncating tests and adding `src/__init__.py`. This targets the destroyed test file.
   - It gives an edge-case matrix for parser functions and recommends `re.fullmatch`. This targets the unfixed bug: the original regex is unanchored and `findall` silently skips garbage.
   - It records the verified facts for this workspace. The original regex omits `s`, and the docstring clauses are listed. The existing test only covers "1h30m". Whether whitespace is allowed between a number and its own unit is not stated, so the skill tells the agent to pick the stricter reading and say so.
   - It requires copying the final file to the task-named output path and diffing the copy. This targets the missing `output/durations.py`.
2. `systemprompt.md` gets a trigger line that names the skill, plus a short rule never to overwrite tests and to run `python3 -m pytest tests -q`. The `README` placeholders, `guardrails.md`, `LongTermMEMORY.md` and `tool_guidance.md` are unchanged.