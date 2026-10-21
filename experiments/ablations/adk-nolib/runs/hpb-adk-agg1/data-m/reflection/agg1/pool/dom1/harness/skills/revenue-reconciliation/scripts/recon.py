#!/usr/bin/env python3
"""Monthly net revenue in USD from transactions, refunds and daily FX.
usage: python3 recon.py SRC_DIR YYYY-MM [OUT_JSON]
Prints every exclusion/anomaly so each can be reviewed; writes OUT_JSON if given."""
import csv, json, sys
src, month = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else None
num = lambda s: float(s.replace(",", "").strip())
fx = {(r["date"], r["currency"].strip().upper()): float(r["usd_per_unit"])
      for r in csv.DictReader(open(f"{src}/fx_daily.csv"))}
def rate(d, c):
    v = fx.get((d, c.strip().upper()))
    if not v:
        print(f"WARN missing/zero fx {c} {d}: {v}"); raise SystemExit(1)
    return v
seen, tx, cur = {}, 0.0, {}
n = 0
for r in csv.DictReader(open(f"{src}/transactions.csv")):
    t = r["txn_id"].strip()
    if t in seen:
        same = seen[t] == r
        print(f"DUP txn {t} ({'identical' if same else 'CONFLICTING - decide'}): dropped later row")
        continue
    seen[t] = r
    cur[t] = r["currency"].strip().upper()
    if r["status"].strip().upper() == "SETTLED" and r["settled_on"].startswith(month):
        tx += num(r["amount"]) * rate(r["settled_on"], r["currency"]); n += 1
    elif r["status"].strip().upper() == "SETTLED" and not r["settled_on"]:
        print(f"WARN settled without date {t}")
rf, m = 0.0, 0
for r in csv.DictReader(open(f"{src}/refunds.csv")):
    t = r["txn_id"].strip()
    if t not in cur:
        print(f"WARN refund {r['refund_id']} has no transaction {t}"); continue
    if r["refunded_on"].startswith(month):
        rf += num(r["amount"]) * rate(r["refunded_on"], cur[t]); m += 1
        if seen[t]["status"].strip().upper() != "SETTLED":
            print(f"WARN refund {r['refund_id']} on non-SETTLED txn {t}")
res = {"net_usd": round(tx - rf, 2), "transactions": n, "refunds": m}
print(f"gross={tx:.4f} refunds={rf:.4f}", res)
if out:
    json.dump(res, open(out, "w"))
