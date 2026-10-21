#!/usr/bin/env python3
"""Net settled revenue in USD for one month from a payment export + fx table.

Usage: python3 scripts/net_revenue.py [transactions.csv] [fx.csv] [YYYY-MM] [output/answer.json]
Defaults: transactions.csv fx.csv 2026-09 output/answer.json
Stdlib only (pandas is NOT installed and pip times out). Writes the answer file,
re-reads it, and prints a summary plus every skipped/duplicate row.
Exits 1 with a message on any unparseable amount/date/currency (never guesses).
"""
import csv, json, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

DATE_FORMATS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d"]


def parse_date(s):
    s = s.strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            pass
    sys.exit(f"unparseable date: {s!r} -- add its format to DATE_FORMATS")


def parse_amount(s):
    t = s.strip().replace(",", "").replace("$", "").replace(" ", "")
    neg = t.startswith("(") and t.endswith(")")  # accounting negative: (954.34)
    t = t.strip("()")
    try:
        v = Decimal(t)
    except Exception:
        sys.exit(f"unparseable amount: {s!r}")
    return -v if neg else v


def main():
    a = sys.argv[1:]
    tx = a[0] if len(a) > 0 else "transactions.csv"
    fxp = a[1] if len(a) > 1 else "fx.csv"
    month = a[2] if len(a) > 2 else "2026-09"
    out = a[3] if len(a) > 3 else "output/answer.json"
    y, m = map(int, month.split("-"))

    with open(fxp, newline="") as f:
        fx = {r["currency"].strip().upper(): Decimal(r["usd_per_unit"]) for r in csv.DictReader(f)}

    seen, total, n = {}, Decimal(0), 0
    with open(tx, newline="") as f:
        for r in csv.DictReader(f):
            tid = r["txn_id"].strip()
            key = tuple(v.strip() for v in r.values())
            if tid in seen:
                tag = "exact duplicate" if seen[tid] == key else "CONFLICTING duplicate (first kept)"
                print(f"skip {tid}: {tag}: {key}")
                continue
            seen[tid] = key
            d = parse_date(r["date"])
            st = r["status"].strip().upper()
            if st != "SETTLED" or (d.year, d.month) != (y, m):
                continue
            cur = r["currency"].strip().upper()
            if cur not in fx:
                sys.exit(f"no fx rate for {cur!r}")
            total += parse_amount(r["amount"]) * fx[cur]
            n += 1

    net = float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    with open(out, "w") as f:
        json.dump({"net_usd": net, "transactions": n}, f)
    with open(out) as f:
        back = json.load(f)
    assert isinstance(back, dict) and set(back) == {"net_usd", "transactions"}
    print(f"unique txn_ids: {len(seen)}; wrote {out}: {back}")


if __name__ == "__main__":
    main()
