Change: `skills/invoice-totals/SKILL.md` rewritten. The "Workspace facts (issue #142 ...)" block is removed. It held this instance's expected outputs (59.97 / 6.00 / 10.79 / 64.76), the test name and its "20.00" assertion, the RATES values, and the KeyError-to-ValueError mapping.

Replacements, all checks the agent re-derives:
- The issue example is now "recompute by hand from the doc's rules and confirm the code's output matches", with no stored numbers.
- Rates are "read from the code's rate table", not listed.
- Return types are "check the doc and any test assertion", not "the test asserts a string".
- The unknown-region rule is generic: a dict KeyError is not the doc's named exception, so map it to the doc's type.
- The doc path is "locate by listing the tree (usually under docs/)", not hard-coded.

Kept unchanged: the generic Decimal and float rounding traps (ROUND_HALF_EVEN default, Decimal(float) noise, round(0.125, 2) = 0.12). These are Python facts, not instance facts. The trigger line in `systemprompt.md` line 5 still names `invoice-totals`. Nothing else was edited.

Evidence for keeping the skill: base1 never loaded it. It went straight to editing and never reran the tests or wrote output/CHANGES.md. The always-on prompt already covers both checks, so I did not add prose for them.

Also, the one-line deletion of an earlier "discount base" bullet was my own cleanup, not driven by a trajectory. It was vague and not checkable.