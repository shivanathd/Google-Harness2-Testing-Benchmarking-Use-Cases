This revision fixes the rejection by removing the instance-specific facts from `skills/fix-python-issue/SKILL.md`.

- **Removed:** the "Workspace facts: `stock` package" block. It listed this instance's file names, which bug sits in which function, the report format string and the `--low` semantics. The description's "verified facts about the `stock` inventory CLI workspace" line is gone too.
- **Replaced with:** a short "Re-derive from the source (do not assume)" section. It tells the agent to map each issue item to its cause, and to note which calls run unconditionally in `main` and which commands return before saving. It also tells the agent to check existing output format, sort order and test assertions before editing, and to leave argparse usage errors alone unless the issue says otherwise.
- **Generalised:** the remaining stock-specific wording in the checklist and probes. This covers `store.save`, `ops.*`, SKU, quantity, `report --low` and `tests/test_stock_extra.py`. The probes now use generic phrasing such as "read-only command on a missing file", "unknown key" and "exact limit". A grep for "stock" and "sku" in the file returns nothing.
- **Unchanged:** the validate-before-mutate rule, the exact `ValueError` and `error:` to stderr with return 1 contract, the backward-compatibility diff, and the probe list. These came from the earlier edit.
- **Trigger line:** the `fix-python-issue` trigger line in `systemprompt.md` is untouched.

I did not re-read the trajectories this round. The edit only removes and generalises text.