#!/usr/bin/env python3
"""Recognised revenue for one month from charges + chargebacks + fx + customers (stdlib only).
Usage: python3 recognise.py --month 2026-09 [--dir .] [--out output/answer.json]
Prints diagnostics (every row's classification) to stderr, writes the JSON answer."""
import argparse, csv, json, os, sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

ZERO_DEC = {"JPY", "KRW", "VND", "CLP", "ISK", "UGX", "XOF", "XAF"}
THREE_DEC = {"BHD", "KWD", "OMR", "JOD", "TND"}

def utc(s):
    s = s.strip().replace("Z", "+00:00")
    d = datetime.fromisoformat(s)
    if d.tzinfo is None:
        sys.exit("naive timestamp, no offset: " + s)
    return d.astimezone(timezone.utc)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True)
    ap.add_argument("--dir", default=".")
    ap.add_argument("--out", default="output/answer.json")
    ap.add_argument("--fee", default="15.00")
    ap.add_argument("--cb-key", default="chargebacks")
    a = ap.parse_args()
    rd = lambda f: list(csv.DictReader(open(os.path.join(a.dir, f), newline="")))
    fx = {r["currency"].strip(): Decimal(r["usd_per_unit"]) for r in rd("fx.csv")}
    test = {r["customer_id"].strip() for r in rd("customers.csv") if r["is_test"].strip().lower() == "true"}
    seen, charges = set(), {}
    for r in rd("charges.csv"):
        if r["charge_id"] in seen:
            print("DUPLICATE charge_id", r["charge_id"], file=sys.stderr)
        seen.add(r["charge_id"]); charges[r["charge_id"]] = r

    def usd(r):
        c = r["currency"].strip()
        dec = 0 if c in ZERO_DEC else 3 if c in THREE_DEC else 2
        return Decimal(r["amount_minor"]) / (Decimal(10) ** dec) * fx[c]

    net, n, k = Decimal(0), 0, 0
    for cid, r in charges.items():
        st = r["status"].strip()
        if st not in ("captured", "authorized", "voided"):
            print("UNKNOWN STATUS", cid, st, file=sys.stderr)
        if st != "captured":
            continue
        t = utc(r["captured_at"]); m = t.strftime("%Y-%m")
        tag = "TEST-EXCLUDED" if r["customer_id"] in test else ("RECOGNISED" if m == a.month else "other month")
        print("%-5s %s %s -> %s UTC  %-13s usd=%s" % (cid, r["currency"], r["captured_at"], t.strftime("%Y-%m-%d %H:%M"), tag, usd(r)), file=sys.stderr)
        if tag == "RECOGNISED":
            n += 1; net += usd(r)
    for cb in rd("chargebacks.csv"):
        r = charges.get(cb["charge_id"])
        if r is None:
            print("ORPHAN chargeback", cb["chargeback_id"], file=sys.stderr); continue
        t = utc(cb["chargeback_at"]); m = t.strftime("%Y-%m")
        tag = "TEST-EXCLUDED" if r["customer_id"] in test else ("BOOKED" if m == a.month else "other month")
        print("%-5s %s chargeback_at=%s %-13s charge=%s status=%s usd=%s" % (cb["chargeback_id"], cb["charge_id"], t.strftime("%Y-%m-%d %H:%M"), tag, r["captured_at"], r["status"], usd(r)), file=sys.stderr)
        if r["status"].strip() != "captured":
            print("  WARNING: chargeback on non-captured charge", file=sys.stderr)
        if tag == "BOOKED":
            k += 1; net -= usd(r) + Decimal(a.fee)
    net = net.quantize(Decimal("0.01"), ROUND_HALF_UP)
    print("net=%s transactions=%d %s=%d" % (net, n, a.cb_key, k), file=sys.stderr)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as f:
        f.write('{"net_usd": %s, "transactions": %d, "%s": %d}\n' % (net, n, a.cb_key, k))

main()
