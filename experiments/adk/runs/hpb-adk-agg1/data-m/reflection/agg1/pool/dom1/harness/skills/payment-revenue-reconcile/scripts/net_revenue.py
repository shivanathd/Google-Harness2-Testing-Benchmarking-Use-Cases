#!/usr/bin/env python3
"""Net revenue for one month from transactions + refunds + daily FX (stdlib only).

usage: net_revenue.py TRANSACTIONS.csv REFUNDS.csv FX_DAILY.csv YYYY-MM [--status SETTLED]
Revenue: unique txn_id, status == SETTLED, settled_on in month, amount * rate(settled_on, currency).
Refunds: refunded_on in month, currency taken from the original txn, rate(refunded_on, currency).
Prints an audit and a JSON line {"net_usd", "transactions", "refunds"}. Stops loudly on anything it
cannot parse or look up (bad amount/date, missing FX row, zero rate, refund with unknown txn_id).
It does not write the deliverable.
"""
import csv, re, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from collections import Counter

DATE_FORMATS = ("%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d")


def parse_amount(s):
    t = s.strip().replace("$", "").replace(" ", "")
    neg = (t.startswith("(") and t.endswith(")")) or t.startswith("-") or t.endswith("-")
    t = re.sub(r"[()\-,]", "", t)
    if not re.fullmatch(r"\d+(\.\d+)?", t):
        sys.exit(f"UNPARSEABLE AMOUNT: {s!r}")
    v = Decimal(t)
    return -v if neg else v


def parse_date(s):
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s.strip(), f).date()
        except ValueError:
            pass
    sys.exit(f"UNPARSEABLE DATE: {s!r}")


def rate(fx, d, cur, what):
    r = fx.get((d, cur))
    if r is None:
        sys.exit(f"NO FX RATE for {cur} on {d} ({what}) -- decide explicitly, do not guess")
    if r <= 0:
        sys.exit(f"NON-POSITIVE FX RATE {r} for {cur} on {d} ({what})")
    return r


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    status = "SETTLED"
    if "--status" in sys.argv:
        status = sys.argv[sys.argv.index("--status") + 1]
        args.remove(status)
    tx_path, rf_path, fx_path, ym = args[:4]
    year, month = map(int, ym.split("-"))
    fx = {}
    for r in csv.DictReader(open(fx_path, newline="")):
        key = (parse_date(r["date"]), r["currency"].strip().upper())
        if key in fx and fx[key] != Decimal(r["usd_per_unit"]):
            print(f"CONFLICTING FX ROW {key}")
        fx[key] = Decimal(r["usd_per_unit"])
    rows = list(csv.DictReader(open(tx_path, newline="")))
    print(f"txn rows={len(rows)} status={dict(Counter(r['status'].strip() for r in rows))}")
    uniq = {}
    for r in rows:
        k = r["txn_id"].strip()
        if k in uniq and uniq[k] != r:
            print(f"CONFLICTING DUPLICATE {k}: {uniq[k]} vs {r} -- decide explicitly")
        uniq.setdefault(k, r)
    dups = sorted(k for k, c in Counter(r["txn_id"].strip() for r in rows).items() if c > 1)
    print(f"unique txn_ids={len(uniq)}; duplicated ids collapsed: {dups}")

    rev, n, excl = Decimal(0), 0, Counter()
    for k, r in uniq.items():
        if r["status"].strip().upper() != status.upper():
            excl["status " + r["status"].strip()] += 1
            continue
        if not r["settled_on"].strip():
            excl["SETTLED but blank settled_on"] += 1
            print(f"  WARN {k} {status} with blank settled_on")
            continue
        d = parse_date(r["settled_on"])
        if (d.year, d.month) != (year, month):
            excl["settled outside month"] += 1
            continue
        cur = r["currency"].strip().upper()
        usd = parse_amount(r["amount"]) * rate(fx, d, cur, k)
        rev += usd
        n += 1
        print(f"  incl {k} {d} {r['amount']} {cur} -> {usd:.4f}")
    print(f"excluded txns: {dict(excl)}")

    ref, m, rexcl = Decimal(0), 0, Counter()
    rrows = list(csv.DictReader(open(rf_path, newline="")))
    rids = Counter(r["refund_id"].strip() for r in rrows)
    print(f"refund rows={len(rrows)} duplicated refund_ids={[k for k, c in rids.items() if c > 1]}")
    seen = set()
    for r in rrows:
        rid = r["refund_id"].strip()
        if rid in seen:
            rexcl["duplicate refund_id"] += 1
            continue
        seen.add(rid)
        d = parse_date(r["refunded_on"])
        if (d.year, d.month) != (year, month):
            rexcl["issued outside month"] += 1
            continue
        t = uniq.get(r["txn_id"].strip())
        if t is None:
            sys.exit(f"REFUND {rid} references unknown txn_id {r['txn_id']}")
        cur = t["currency"].strip().upper()
        usd = parse_amount(r["amount"]) * rate(fx, d, cur, rid)
        ref += usd
        m += 1
        print(f"  refund {rid} {r['txn_id']} {d} {r['amount']} {cur} -> {usd:.4f}"
              f" (orig status {t['status'].strip()}, settled_on {t['settled_on'] or '-'})")
    print(f"excluded refunds: {dict(rexcl)}")
    print(f"gross_usd={rev:.4f} refunds_usd={ref:.4f}")
    print('{"net_usd": %s, "transactions": %d, "refunds": %d}' % ((rev - ref).quantize(Decimal("0.01"), ROUND_HALF_UP), n, m))


main()
