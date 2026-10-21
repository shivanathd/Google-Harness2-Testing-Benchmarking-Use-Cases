KEEP_BASE. I changed no files.

- **Both runs match.** base1 and base2 produced the same `output/answer.json`: `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`. I did not recompute the figure independently. My check was limited to base1's printed intermediates, which are internally consistent.
- **Both followed the same workflow.** Each read POLICY.md and the four CSVs. Each then wrote one Decimal-based script that did four things:
  - converted `captured_at` to UTC before assigning the month;
  - excluded test customers from charges and chargebacks;
  - booked chargebacks by `chargeback_at` in UTC;
  - rounded only the final figure.

  Each then wrote the JSON in the requested shape, with no extra fields.
- **The one slip was self-corrected.** In base1's first script the fee sign was wrong (`usd - 15`, which gave 5162.12). The agent caught it on re-reading its own output and fixed it before writing the file (`usd + 15`, which gave 5072.12). Because it was a one-off arithmetic slip, caught within the run, it doesn't justify a script, skill or plugin. Adding always-on text would cost context on every run for no demonstrated gain.
- **Existing components are fine.** The system prompt already says to write deliverables under `output/`, and both runs did. Neither run hit a tool error, a timeout or a missing-deliverable problem.