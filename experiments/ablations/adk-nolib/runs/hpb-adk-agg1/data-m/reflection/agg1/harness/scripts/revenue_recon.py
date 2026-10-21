#!/usr/bin/env python3
"""Compute monthly net USD revenue from transactions/refunds/fx CSVs and write answer.json.

usage: python3 scripts/revenue_recon.py <data_dir> <YYYY-MM> [out_path]
  data_dir  holds transactions.csv, refunds.csv, fx_daily.csv
  out_path  default output/answer.json

Rules: dedupe transactions by txn_id (first row kept; conflicting duplicates are reported),
amounts may contain thousands commas, only status SETTLED with settled_on in the month counts
(rate on settled_on); refunds dated in the month reduce revenue (rate on refunded_on, currency of
the original transaction). Exits 1 on a missing fx rate, zero rate, unknown refund txn or bad amount;
nothing is written in that case. Prints a per-row breakdown to stdout.
"""
import csv, json, os, sys
from decimal import Decimal as D, ROUND_HALF_UP


def die(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def num(s):
    try:
        return D(s.replace(",", "").strip())
    except Exception:
        die("bad amount %r" % s)


def main():
    if len(sys.argv) < 3:
        die(__doc__)
    d, month = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else "output/answer.json"
    rd = lambda n: list(csv.DictReader(open(os.path.join(d, n), newline="")))
    txns, refunds, fxrows = rd("transactions.csv"), rd("refunds.csv"), rd("fx_daily.csv")
    fx = {(r["date"].strip(), r["currency"].strip()): D(r["usd_per_unit"]) for r in fxrows}

    def rate(date, cur):
        r = fx.get((date, cur))
        if r is None or r <= 0:
            die("no usable fx rate for %s %s" % (date, cur))
        return r

    uniq = {}
    for r in txns:
        k = r["txn_id"].strip()
        if k in uniq:
            if uniq[k] != r:
                print("WARN conflicting duplicate txn_id %s: %s vs %s" % (k, uniq[k], r))
            continue
        uniq[k] = r
    print("rows=%d unique_txn_ids=%d" % (len(txns), len(uniq)))

    total, n = D(0), 0
    for k, r in uniq.items():
        if r["status"].strip().upper() == "SETTLED" and r["settled_on"].strip().startswith(month):
            usd = num(r["amount"]) * rate(r["settled_on"].strip(), r["currency"].strip())
            total += usd; n += 1
            print("TXN %s %s %s %s -> %.4f" % (k, r["settled_on"], r["amount"], r["currency"], usd))
    rtotal, m = D(0), 0
    for r in refunds:
        if r["refunded_on"].strip().startswith(month):
            t = uniq.get(r["txn_id"].strip())
            if t is None:
                die("refund %s references unknown txn %s" % (r["refund_id"], r["txn_id"]))
            usd = num(r["amount"]) * rate(r["refunded_on"].strip(), t["currency"].strip())
            rtotal += usd; m += 1
            print("REF %s %s %s %s %s -> %.4f" % (r["refund_id"], r["txn_id"], r["refunded_on"], r["amount"], t["currency"], usd))
    net = (total - rtotal).quantize(D("0.01"), ROUND_HALF_UP)
    print("gross=%.4f refunds=%.4f net=%s txns=%d refunds_applied=%d" % (total, rtotal, net, n, m))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    json.dump({"net_usd": float(net), "transactions": n, "refunds": m}, open(out, "w"))
    print("wrote", out)


main()
