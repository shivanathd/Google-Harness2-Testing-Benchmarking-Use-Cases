**Base run (base1).** It produced a correct answer. I recomputed the figures independently from the source logs and got the same numbers:
- gateway: 96 requests, error rate 0.1354, p95 334
- search: 119 requests, error rate 0.1513, p95 192
- billing: 124 requests, error rate 0.1613, p95 393

I also checked the billing schema change. All `latency_s` rows fall at or after 09:00 UTC, and no `latency_ms` rows fall after it. The run did the following right:
- It converted mixed UTC offsets before windowing.
- It skipped truncated lines.
- It excluded `/healthz`.
- It counted only status ≥ 500 as errors.
- It converted seconds to milliseconds per row.
- It used nearest-rank p95.

I found nothing to fix, so the base behaviour is preserved.

**Added `skills/service-traffic-report/SKILL.md`.** This is a low-risk, on-demand skill for the next log-statistics task in this ops domain. It gives the order of operations (parse, drop probes, convert to UTC, apply a start-inclusive and end-exclusive window, then count). It also carries:
- the per-row unit normalisation and a check that the runbook's cut-over agrees with the data;
- nearest-rank p95 with float-safe rounding;
- a pre-finish consistency check, plus the workspace facts verified here, labelled as such.

The motivating moments in the trajectory:
- the mixed `-03:00`, `+01:00` and `+00:00` offsets, which the runbook never mentions;
- the sanity check of `latency_s` against `latency_ms` ranges;
- the truncated lines.

**Trigger line.** I appended one line to `systemprompt.md` so the skill is named in the always-on text.

I made no other edits: no always-on prose beyond that one line, and no scripts, since procedure belongs to the parallel candidate.