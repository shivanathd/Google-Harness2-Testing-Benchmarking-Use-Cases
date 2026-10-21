component: LongTermMEMORY.md
candidates: c2, dom2
change: Went from empty to a short "Finance-export reconciliation conventions" note. It has two rules. The first is to convert each line at full precision, sum unrounded, and round the reported total once. The second is to take the counts from the same filtered, de-duplicated set the total came from. c2 and dom2 carry the identical text.
observed: Both rollouts wrote `{"net_usd": 24317.47, "transactions": 16, "refunds": 5}`. Neither shows the note steering anything. dom2's script (line 101) and c2's summary (line 151) sum at full Decimal precision and round once. Neither cites the note, though dom2 may simply have chosen that on its own. The runs that did round per line were inv1 (line 195) and inv2 (line 98), and both ended at 24317.48. Both of those ran the empty base memory, so the edit never faced the failure it targets. Six unedited runs (base1, base2, c1, dom1, inv1, inv2) split 4 to 2 between .47 and .48. base2 rounded per line and still got .47. No single execution isolates the note, and each edited candidate has one rollout.
verdict: confounded
component: scripts/ and skills/ (README.md placeholders)
candidates: c1, dom1, inv1, inv2, c2, dom2
change: These directories hold only a README and are the same in every candidate. They were never an edit. The c1, dom1, inv1 and inv2 diffs are empty, so c1, the adopted candidate, is identical to the base.
observed: There is nothing to contrast. All the rollouts handled the data traps without help. The traps were duplicate txn_ids, comma-formatted amounts, PENDING and VOID rows, and settle-day and refund-day FX rates. The deliverable shape was correct in every run. The only divergence anywhere was the one-cent rounding split described above.
verdict: no observed effect
