# Library — swe

Each entry is an earlier task in THIS domain whose harness was chosen, stored with its FULL component tree and why it was picked. Browse this index, then open the entries that look relevant to the matter in front of you.

## `harnesses/swe-e/`
- harness: `harnesses/swe-e/harness/` — 1 skills, 1 scripts, 1 hooks; 1,371 always-on chars
- why:     `harnesses/swe-e/EXPERIENCE.md`
- cue:     A small-repo bug-fix task where the agent has a hard LLM-call budget and reports success from weak checks. The agent re-writes the file unchanged and re-runs probes that print the wrong output, and prompt or skill text asking for a "real edit" or "verify the output" has no visible effect.

## `harnesses/swe-h/`
- harness: `harnesses/swe-h/harness/` — 1 skills, 1 scripts, 1 hooks; 2,017 always-on chars
- why:     `harnesses/swe-h/EXPERIENCE.md`
- cue:     A harness adds prose rules ("implement every item", "re-read the issue", "only claim what you ran") plus a Stop-time check, to an agent that finishes with a confident summary of work it did not do or verify.

## `harnesses/swe-m/`
- harness: `harnesses/swe-m/harness/` — 1 skills, 1 scripts, 1 hooks; 2,539 always-on chars
- why:     `harnesses/swe-m/EXPERIENCE.md`
- cue:     A bug-fix harness where the issue lists a few symptoms and a spec document gives the full contract. The agent reaches "the existing test passes" and finishes, even though the spec has several other violations that no test or hook measures.
