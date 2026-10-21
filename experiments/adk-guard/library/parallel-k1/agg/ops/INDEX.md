# Library — ops

Each entry is an earlier task in THIS domain whose harness was chosen, stored with its FULL component tree and why it was picked. Browse this index, then open the entries that look relevant to the matter in front of you.

## `harnesses/ops-e/`
- harness: `harnesses/ops-e/harness/` — 1 skills; 376 always-on chars
- why:     `harnesses/ops-e/EXPERIENCE.md`
- cue:     A task asks for exact counts, distinct values or top-N over a noisy, mixed-format record file. The file has look-alike lines, such as continuation lines or quoted levels, and mixed timezone offsets. The baseline harness gives no computation guidance, so the agent reads the file and answers from the raw text.

## `harnesses/ops-h/`
- harness: `harnesses/ops-h/harness/` — 1 skills; 791 always-on chars
- why:     `harnesses/ops-h/EXPERIENCE.md`
- cue:     A task that needs exact statistics from large or compressed logs, with several hidden traps (mixed timezones, truncated lines, probe traffic, a mid-window unit change). The base harness has no computation path, and the agent tries to read the data through its own context under a tight call limit.

## `harnesses/ops-m/`
- harness: `harnesses/ops-m/harness/` — 1 skills; 1,032 always-on chars
- why:     `harnesses/ops-m/EXPERIENCE.md`
- cue:     A recurring analysis task over messy, multi-file inputs (retries, mixed timezones, compressed rotations, look-alike lines) where an unaided run flailed with ad-hoc shell commands and wrote no deliverable.
