Checks to re-derive on every bug-fix task (the issue lists symptoms; the cited spec lists the contract):
- Turn each bullet of the cited doc/spec into one probe and run it, not just the issue's examples: return types and output format, rounding mode, case handling, error type for invalid input.
- Compare the current code's return types with the spec's, not only the reported symptoms; a symptom list is usually a subset of the divergences.
- Run the issue's own example before and after the edit, and confirm the output changed as intended.
- Deliverable is the file the task names (here output/CHANGES.md); fix the source in place and keep public names and signatures.
