# Guardrails for log-analysis / counting tasks
- Compute answers with a short script (python3), never by eyeballing the log.
- A log event starts only at a line beginning with a timestamp. Indented/continuation lines (stack traces) belong to the previous event; never count them and never take level, user, or code from them.
- Take level, user, and code from the event's own fields, not from words in free-text `msg=` (e.g. "retrying after ERROR" is not an ERROR event).
- Timestamps carry offsets: convert every one to UTC before windowing. Windows are start-inclusive, end-exclusive.
- Check for ties in "most frequent" answers and for malformed lines; print the matched events to sanity-check them.
- Write the deliverable in exactly the requested schema and types (ints as ints) under output/, then re-read it.
