This revision fixes the rejection. I did not re-read the trajectories; the edit only removes the instance data and keeps the method.

- I deleted the "Workspace facts" block from `skills/service-traffic-stats/SKILL.md`. It held this task's results: the per-service requests, error rates and p95 values for the 06:00–12:00Z window, the 09:03 and 08:53 UTC unit-switch times, and the service names and the ~25% `/healthz` share. I replaced it with one line telling the agent to re-derive which services carry which latency field, whether any service mixes both units in the window, and that the probe route is removed before counting.
- I replaced the hard-coded window in the helper command with `<START_UTC> <END_UTC>`.
- I generalised the offset example to "a +01:00 stamp is one hour earlier in UTC".
- I generalised the units check to "the `units=` census shows which fields each service carries; a service that switched units must show both".
- I changed the final check from "exactly the three service keys" to "one key per service file".
- The method rules are unchanged. These are the RUNBOOK precedence, half-open UTC window, probe exclusion, error = status ≥ 500, per-record unit conversion with whole-ms rounding, nearest-rank p95, and the 4-decimal error rate.
- The trigger line in `systemprompt.md` is unchanged, and the helper script already ships under `skills/service-traffic-stats/scripts/`. A grep of the helper for the removed values and the instance service names found nothing. The only date in it is a generic example in its usage docstring, so I left it.