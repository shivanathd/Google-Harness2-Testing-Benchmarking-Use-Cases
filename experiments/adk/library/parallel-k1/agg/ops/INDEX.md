# Library — ops

Each entry is an earlier task in THIS domain whose harness was chosen, stored with its FULL component tree and why it was picked. Browse this index, then open the entries that look relevant to the matter in front of you.

## `harnesses/ops-e/`
- harness: `harnesses/ops-e/harness/` — 1 skills; 434 always-on chars
- why:     `harnesses/ops-e/EXPERIENCE.md`
- cue:     A deliverable is a set of counts or rankings computed from a long, messy raw file. The file has traps such as continuation lines, lookalike substrings, mixed timezones and window edges. The base agent read the file once and wrote the number from that read.

## `harnesses/ops-h/`
- harness: `harnesses/ops-h/harness/` — 1 skills; 1,060 always-on chars
- why:     `harnesses/ops-h/EXPERIENCE.md`
- cue:     A harness that is nearly empty is given a mechanical, multi-rule data-processing task (parse logs, filter, aggregate, compute a percentile). The baseline spends its tool-call budget re-reading raw inputs by eye and never runs code or produces the deliverable.

## `harnesses/ops-m/`
- harness: `harnesses/ops-m/harness/` — 1 skills; 842 always-on chars
- why:     `harnesses/ops-m/EXPERIENCE.md`
- cue:     A task over raw operational data, such as rotated or compressed logs, with mixed time zones, retries and tricky continuation lines. The unit of analysis (a request) differs from the unit of the raw rows (a line). A baseline run read the data by eye or with ad-hoc shell and delivered nothing.
