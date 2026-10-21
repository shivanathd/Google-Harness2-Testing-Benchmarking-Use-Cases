#!/usr/bin/env python3
"""Net settled revenue in USD for one month from a payment export + fx table.

Usage: python3 scripts/settled_revenue.py --month 2026-09 [--status SETTLED]
         [--transactions transactions.csv] [--fx fx.csv] [--out output/answer.json] [--dry-run]

Stdlib only (pandas is not installed). Handles mixed date formats, thousands
separators, accounting negatives "(1,234.50)", currency symbols, and repeated
txn_id rows (one transaction = one row; conflicting repeats are reported).
Fails loudly (exit 2, nothing written) on an unparseable date/amount or a
currency missing from the fx table, listing the offending rows.
Writes {"net_usd": x.xx, "transactions": n}, re-reads it, and prints an audit.
"""
import argparse, csv, json, re, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

DATE_FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y", "%B %d, %Y", "%d %b %Y", "%d %B %Y",
                "%m/%d/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]


def parse_date(s):
    s = s.strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    raise ValueError("unparseable date %r" % s)


def parse_amount(s):
    t = s.strip()
    neg = t.startswith("(") and t.endswith(")") or t.startswith("-") or t.endswith("-")
    t = re.sub(r"[^0-9.]", "", t)
    if not t:
        raise ValueError("unparseable amount %r" % s)
    v = Decimal(t)
    return -v if neg else v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True, help="YYYY-MM")
    ap.add_argument("--status", default="SETTLED")
    ap.add_argument("--transactions", default="transactions.csv")
    ap.add_argument("--fx", default="fx.csv")
    ap.add_argument("--out", default="output/answer.json")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    year, mon = (int(x) for x in a.month.split("-"))

    with open(a.fx, newline="") as f:
        fx = {r["currency"].strip().upper(): Decimal(r["usd_per_unit"].strip()) for r in csv.DictReader(f)}
    with open(a.transactions, newline="") as f:
        rows = list(csv.DictReader(f))

    seen, bad, dup_exact, dup_conflict = {}, [], 0, []
    for i, r in enumerate(rows, start=2):
        try:
            d = parse_date(r["date"])
            amt = parse_amount(r["amount"])
            cur = r["currency"].strip().upper()
            if cur not in fx:
                raise ValueError("currency %r not in fx table" % cur)
        except ValueError as e:
            bad.append("line %d %s: %s" % (i, r.get("txn_id"), e))
            continue
        rec = (d, amt, cur, r["status"].strip().upper())
        tid = r["txn_id"].strip()
        if tid in seen:
            if seen[tid] == rec:
                dup_exact += 1
            else:
                dup_conflict.append("%s: kept first %s, ignored %s" % (tid, seen[tid], rec))
            continue
        seen[tid] = rec
    if bad:
        print("ERROR: fix these rows (do not guess), nothing written:\n  " + "\n  ".join(bad))
        sys.exit(2)

    total, n, skipped = Decimal(0), 0, {}
    for tid, (d, amt, cur, st) in sorted(seen.items()):
        if st != a.status.upper() or (d.year, d.month) != (year, mon):
            key = "status=%s" % st if st != a.status.upper() else "other month"
            skipped[key] = skipped.get(key, 0) + 1
            continue
        total += amt * fx[cur]
        n += 1
    net = float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    print("rows=%d unique_txn_ids=%d exact_duplicate_rows_dropped=%d" % (len(rows), len(seen), dup_exact))
    for c in dup_conflict:
        print("WARNING conflicting repeat of txn_id -> " + c)
    print("excluded (unique txns): %s" % skipped)
    print("included=%d net_usd=%.2f" % (n, net))
    if a.dry_run:
        return
    with open(a.out, "w") as f:
        json.dump({"net_usd": net, "transactions": n}, f)
    with open(a.out) as f:
        back = json.load(f)
    assert back == {"net_usd": net, "transactions": n}, back
    print("wrote and re-read %s: %s" % (a.out, back))


if __name__ == "__main__":
    main()
