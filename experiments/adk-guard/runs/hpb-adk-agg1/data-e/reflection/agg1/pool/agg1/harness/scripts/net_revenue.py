#!/usr/bin/env python3
"""Net settled revenue in USD for one month from a payment export + fx table.

Usage: python3 scripts/net_revenue.py [--tx transactions.csv] [--fx fx.csv]
           --month YYYY-MM [--status SETTLED] [--out output/answer.json] [--dry]

Standard library only (pandas may be missing). Handles: ISO and 'Mon DD, YYYY'
dates, thousands separators, accounting negatives '(1,234.50)', currency
symbols, duplicate txn_id rows (first kept; conflicting duplicates reported).
Writes {"net_usd": <2dp>, "transactions": <count>} and prints a diagnostic
summary to stderr. Exit 1 with a message on any unparseable value, unknown
currency or missing column -- fix the input handling, do not rerun unchanged.
"""
import argparse, csv, json, os, re, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

DATE_FORMATS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%Y/%m/%d", "%m/%d/%Y", "%d %b %Y", "%Y-%m-%dT%H:%M:%S"]


def parse_amount(s):
    t = s.strip()
    neg = t.startswith("(") and t.endswith(")")
    t = re.sub(r"[()\s,$€£₹]", "", t)
    if t.startswith("-"):
        neg, t = True, t[1:]
    try:
        v = Decimal(t)
    except InvalidOperation:
        raise ValueError("unparseable amount %r" % s)
    return -v if neg else v


def parse_date(s):
    t = s.strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(t, f)
        except ValueError:
            pass
    raise ValueError("unparseable date %r" % s)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--tx", default="transactions.csv")
    a.add_argument("--fx", default="fx.csv")
    a.add_argument("--month", required=True, help="YYYY-MM, taken from the task")
    a.add_argument("--status", default="SETTLED")
    a.add_argument("--out", default="output/answer.json")
    a.add_argument("--dry", action="store_true")
    o = a.parse_args()
    year, mon = map(int, o.month.split("-"))

    with open(o.fx, newline="") as f:
        fx = {r["currency"].strip().upper(): Decimal(r["usd_per_unit"].strip()) for r in csv.DictReader(f)}
    with open(o.tx, newline="") as f:
        rows = list(csv.DictReader(f))
    for c in ("txn_id", "date", "amount", "currency", "status"):
        if not rows or c not in rows[0]:
            sys.exit("missing column %s in %s" % (c, o.tx))

    seen, total, n, dupes, conflicts = {}, Decimal(0), 0, 0, []
    for r in rows:
        tid = r["txn_id"].strip()
        key = tuple(r[c].strip() for c in ("date", "amount", "currency", "status"))
        if tid in seen:
            dupes += 1
            if seen[tid] != key:
                conflicts.append(tid)
            continue
        seen[tid] = key
        if r["status"].strip().upper() != o.status.upper():
            continue
        d = parse_date(r["date"])
        if (d.year, d.month) != (year, mon):
            continue
        cur = r["currency"].strip().upper()
        if cur not in fx:
            sys.exit("currency %r (txn %s) not in %s" % (cur, tid, o.fx))
        total += parse_amount(r["amount"]) * fx[cur]
        n += 1

    net = float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    print("rows=%d unique_txn_ids=%d duplicate_rows_dropped=%d conflicting_duplicates=%s included=%d net_usd=%.2f"
          % (len(rows), len(seen), dupes, conflicts or "none", n, net), file=sys.stderr)
    ans = {"net_usd": net, "transactions": n}
    if not o.dry:
        os.makedirs(os.path.dirname(o.out) or ".", exist_ok=True)
        with open(o.out, "w") as f:
            json.dump(ans, f)
    print(json.dumps(ans))


if __name__ == "__main__":
    main()
