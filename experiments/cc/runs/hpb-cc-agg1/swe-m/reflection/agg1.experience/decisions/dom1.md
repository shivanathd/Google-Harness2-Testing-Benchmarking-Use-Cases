KEEP_BASE. I changed no files in `context/harness/`.

- **Evidence:** The only rollout, base1, resolved issue #142 correctly.
  - It read `ISSUE.md` and `docs/ROUNDING.md` before editing.
  - It switched `compute_totals` to `Decimal` with half-up rounding at each step: line gross, line discount and tax.
  - It charged tax on `subtotal - discount`.
  - It made `rate_for` case-insensitive, with unknown regions raising `ValueError`.
  - It kept the public names and signatures, and `line_total` now returns a `Decimal`.
  - It added tests for each reported symptom, and the issue's example returned `{'subtotal': '59.97', 'discount': '6.00', 'tax': '10.79', 'total': '64.76'}`, matching the rules in `ROUNDING.md`.
  - It wrote `output/CHANGES.md`.
- **Only friction:** pytest failed with a sandbox `PermissionError`, so the agent fell back to calling the test functions directly. That is a procedure and environment problem, which another candidate owns. It is not missing domain knowledge.
- **Why no skill:** There was no divergence between runs, no repeated failure, and no visible risk I could trace to a trajectory moment. A skill on money and rounding would be speculative, and it would also need an always-on trigger line.