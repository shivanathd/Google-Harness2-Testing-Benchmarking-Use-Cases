#!/usr/bin/env python3
"""Net revenue in USD for one UTC month: captured charges minus chargebacks and fees.

Usage: python3 scripts/net_revenue.py --month YYYY-MM [--charges charges.csv]
           [--chargebacks chargebacks.csv] [--customers customers.csv] [--fx fx.csv]
           [--fee 15.00] [--out output/answer.json] [--dry]

Standard library only. Rules (POLICY.md of this task family -- re-read the policy and
change flags if it differs): status 'captured' only; month decided on the timestamp
converted to UTC; amount_minor / 10**exponent (JPY 0, others 2); fx = usd_per_unit
multiply; customers with is_test true are dropped from charges AND chargebacks; a
chargeback reverses the full original charge plus a flat fee, both booked in the UTC
month of chargeback_at; "transactions" counts captured charges of the month even if
charged back later. Rounds once at the end. Writes {"net_usd","transactions","chargebacks"}.
Exits 1 on an unparseable value, unknown currency/charge id; diagnostics go to stderr.
"""
import argparse, csv, json, os, sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

EXP = {"JPY": 0, "KRW": 0, "VND": 0, "BHD": 3, "KWD": 3}  # default exponent is 2


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def utc(s):
    t = s.strip().replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(t)
    except ValueError:
        sys.exit("unparseable timestamp %r" % s)
    if d.tzinfo is None:
        sys.exit("timestamp without offset %r (decide deliberately, then edit)" % s)
    return d.astimezone(timezone.utc)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--month", required=True)
    a.add_argument("--charges", default="charges.csv")
    a.add_argument("--chargebacks", default="chargebacks.csv")
    a.add_argument("--customers", default="customers.csv")
    a.add_argument("--fx", default="fx.csv")
    a.add_argument("--fee", default="15.00")
    a.add_argument("--status", default="captured")
    a.add_argument("--out", default="output/answer.json")
    a.add_argument("--dry", action="store_true")
    o = a.parse_args()
    y, m = map(int, o.month.split("-"))
    inm = lambda d: (d.year, d.month) == (y, m)
    fee = Decimal(o.fee)

    fx = {r["currency"].upper(): Decimal(r["usd_per_unit"]) for r in rows(o.fx)}
    test = {r["customer_id"] for r in rows(o.customers) if r["is_test"].lower() == "true"}

    def usd(c, minor):
        if c.upper() not in fx:
            sys.exit("currency %r not in fx table" % c)
        return Decimal(minor) / (Decimal(10) ** EXP.get(c.upper(), 2)) * fx[c.upper()]

    ch, dupc = {}, 0
    for r in rows(o.charges):
        if r["charge_id"] in ch:
            dupc += 1
            continue
        ch[r["charge_id"]] = r
    rev, n, bycur, skipped_test, edge = Decimal(0), 0, {}, [], []
    for cid, r in ch.items():
        d = utc(r["captured_at"])
        if r["status"].lower() != o.status.lower():
            continue
        if r["customer_id"] in test:
            if inm(d):
                skipped_test.append(cid)
            continue
        if r["captured_at"][:7] != d.strftime("%Y-%m") and (inm(d) or r["captured_at"][:7] == o.month):
            edge.append("%s %s->UTC %s" % (cid, r["captured_at"], d.strftime("%Y-%m-%d %H:%M")))
        if not inm(d):
            continue
        v = usd(r["currency"], r["amount_minor"])
        rev += v
        n += 1
        bycur[r["currency"]] = bycur.get(r["currency"], Decimal(0)) + v

    cbs, nc, cb_usd, cb_test, cb_bad, seen = Decimal(0), 0, Decimal(0), [], [], set()
    for r in rows(o.chargebacks):
        if r["chargeback_id"] in seen:
            continue
        seen.add(r["chargeback_id"])
        d = utc(r["chargeback_at"])
        if not inm(d):
            continue
        c = ch.get(r["charge_id"])
        if c is None:
            sys.exit("chargeback %s refers to unknown charge %s" % (r["chargeback_id"], r["charge_id"]))
        if c["customer_id"] in test:
            cb_test.append(r["chargeback_id"])
            continue
        if c["status"].lower() != o.status.lower():
            cb_bad.append(r["chargeback_id"])
        cb_usd += usd(c["currency"], c["amount_minor"]) + fee
        nc += 1

    net = (rev - cb_usd).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    q = lambda v: v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    print("charges=%d dup_rows=%d | revenue_txns=%d revenue_usd=%s by_cur=%s | test_charges_dropped=%s | "
          "utc_month_shifted=%s | chargebacks_applied=%d reversal_plus_fees_usd=%s test_chargebacks_dropped=%s "
          "chargebacks_on_non_%s_charge=%s | net_usd=%s"
          % (len(ch), dupc, n, q(rev), {k: str(q(v)) for k, v in bycur.items()}, skipped_test or "none",
             edge or "none", nc, q(cb_usd), cb_test or "none", o.status, cb_bad or "none", net), file=sys.stderr)
    ans = {"net_usd": float(net), "transactions": n, "chargebacks": nc}
    if not o.dry:
        os.makedirs(os.path.dirname(o.out) or ".", exist_ok=True)
        with open(o.out, "w") as f:
            json.dump(ans, f)
    print(json.dumps(ans))


if __name__ == "__main__":
    main()
