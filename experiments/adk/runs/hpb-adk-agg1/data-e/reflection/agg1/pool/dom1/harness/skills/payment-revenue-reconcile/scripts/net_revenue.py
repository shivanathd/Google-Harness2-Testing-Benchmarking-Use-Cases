#!/usr/bin/env python3
"""Net settled revenue from a payment-processor export + FX table (stdlib only).

usage: net_revenue.py TRANSACTIONS.csv FX.csv YYYY-MM [--status SETTLED]
Prints an audit (dirty-format counts, duplicate ids, exclusions by reason) and a
JSON line {"net_usd": ..., "transactions": ...}. Stops loudly on anything it
cannot parse rather than skipping it.
"""
import csv, re, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from collections import Counter

DATE_FORMATS = ("%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d")


def parse_amount(s):
    t = s.strip().replace("$", "").replace(" ", "")
    neg = t.startswith("(") and t.endswith(")") or t.startswith("-") or t.endswith("-")
    t = re.sub(r"[()\-,]", "", t)
    if not re.fullmatch(r"\d+(\.\d+)?", t):
        sys.exit(f"UNPARSEABLE AMOUNT: {s!r}")
    v = Decimal(t)
    return -v if neg else v


def parse_date(s):
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s.strip(), f)
        except ValueError:
            pass
    sys.exit(f"UNPARSEABLE DATE: {s!r}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    status = "SETTLED"
    if "--status" in sys.argv:
        status = sys.argv[sys.argv.index("--status") + 1]
        args.remove(status)
    tx_path, fx_path, ym = args[:3]
    year, month = map(int, ym.split("-"))
    fx = {r["currency"].strip().upper(): Decimal(r["usd_per_unit"]) for r in csv.DictReader(open(fx_path, newline=""))}
    rows = list(csv.DictReader(open(tx_path, newline="")))
    print(f"rows={len(rows)} status={dict(Counter(r['status'] for r in rows))} currencies={dict(Counter(r['currency'] for r in rows))}")
    iso, odd = r"\d{4}-\d\d-\d\d", r"[(),]"
    print("non-ISO dates=%d paren/comma amounts=%d" % (
        sum(1 for r in rows if not re.fullmatch(iso, r["date"])),
        sum(1 for r in rows if re.search(odd, r["amount"]))))
    uniq = {}
    for r in rows:
        k = r["txn_id"].strip()
        if k in uniq and uniq[k] != r:
            print(f"CONFLICTING DUPLICATE {k}: {uniq[k]} vs {r} -- decide explicitly")
        uniq.setdefault(k, r)
    dups = [k for k, c in Counter(r["txn_id"].strip() for r in rows).items() if c > 1]
    print(f"duplicate txn_ids collapsed to one row: {sorted(dups)}")
    total, n, excl = Decimal(0), 0, Counter()
    for k, r in uniq.items():
        d = parse_date(r["date"])
        if r["status"].strip().upper() != status.upper():
            excl["status"] += 1
        elif (d.year, d.month) != (year, month):
            excl["other month"] += 1
        else:
            cur = r["currency"].strip().upper()
            if cur not in fx:
                sys.exit(f"NO FX RATE for {cur}")
            total += parse_amount(r["amount"]) * fx[cur]
            n += 1
            print(f"  incl {k} {d:%Y-%m-%d} {r['amount']} {cur}")
    print(f"excluded: {dict(excl)}")
    print('{"net_usd": %s, "transactions": %d}' % (total.quantize(Decimal("0.01"), ROUND_HALF_UP), n))


main()
