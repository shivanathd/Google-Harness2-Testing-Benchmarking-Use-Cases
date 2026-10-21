# Library — data

Each entry is an earlier task in THIS domain whose harness was chosen, stored with its FULL component tree and why it was picked. Browse this index, then open the entries that look relevant to the matter in front of you.

## `harnesses/data-e/`
- harness: `harnesses/data-e/harness/` — 1 skills; 635 always-on chars
- why:     `harnesses/data-e/EXPERIENCE.md`
- cue:     A task turns a messy tabular export (mixed date formats, accounting-style negatives, repeated IDs, reference-rate tables) into one or two summary numbers. The base harness has only prose guidance, and an ad hoc script crashes on a malformed value, so the agent loops on it until its call budget runs out and no deliverable gets written.

## `harnesses/data-h/`
- harness: `harnesses/data-h/harness/` — 1 skills; 801 always-on chars
- why:     `harnesses/data-h/EXPERIENCE.md`
- cue:     A base harness with almost no instructions fails an exports-to-figures reconciliation task by skipping computation. It writes a placeholder or malformed deliverable after reading the inputs, and the policy has several fiddly rules (timezone month edges, units, exclusions, fees).

## `harnesses/data-m/`
- harness: `harnesses/data-m/harness/` — 1 skills; 697 always-on chars
- why:     `harnesses/data-m/EXPERIENCE.md`
- cue:     A base run reads the input files and then stops with a prose plan and no deliverable, on a task that is a mechanical multi-file join with many small rules (dedupe, filter dates, FX lookup, refund currency).
