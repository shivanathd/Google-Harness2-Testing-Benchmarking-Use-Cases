#!/usr/bin/env python3
"""Net revenue in USD for one month: settled transactions minus refunds, daily fx.

Usage: python3 scripts/net_revenue.py --month YYYY-MM [--tx transactions.csv]
           [--refunds refunds.csv] [--fx fx_daily.csv] [--out output/answer.json] [--dry]

Standard library only. Rules: a txn_id counts once (first row kept; conflicting
duplicates reported); revenue = status SETTLED, month of settled_on, rate of the
settled_on day; refunds = month of refunded_on, in the original transaction's
currency, rate of the refunded_on day. Amounts may carry thousands commas or
"(x)" negatives. Writes {"net_usd", "transactions", "refunds"}; rounds once at the
end. Diagnostics go to stderr -- read them against the raw files.
"""
import argparse, csv, json, os, re, sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

FMTS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%Y/%m/%d", "%m/%d/%Y", "%d %b %Y", "%Y-%m-%dT%H:%M:%S"]


def amt(s):
    t = s.strip()
    neg = t.startswith("(") and t.endswith(")")
    t = re.sub(r"[()\s,$€£₹]", "", t)
    if t.startswith("-"):
        neg, t = True, t[1:]
    try:
        v = Decimal(t)
    except InvalidOperation:
        sys.exit("unparseable amount %r" % s)
    return -v if neg else v


def day(s):
    t = s.strip()
    for f in FMTS:
        try:
            return datetime.strptime(t, f).date()
        except ValueError:
            pass
    sys.exit("unparseable date %r" % s)


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--month", required=True)
    a.add_argument("--tx", default="transactions.csv")
    a.add_argument("--refunds", default="refunds.csv")
    a.add_argument("--fx", default="fx_daily.csv")
    a.add_argument("--status", default="SETTLED")
    a.add_argument("--out", default="output/answer.json")
    a.add_argument("--dry", action="store_true")
    o = a.parse_args()
    y, m = map(int, o.month.split("-"))
    inm = lambda d: (d.year, d.month) == (y, m)

    fx = {}
    for r in rows(o.fx):
        fx[(day(r["date"]), r["currency"].upper())] = Decimal(r["usd_per_unit"])

    def rate(d, c):
        v = fx.get((d, c.upper()))
        if v is None or v <= 0:
            sys.exit("no usable fx rate for %s on %s (got %r)" % (c, d, v))
        return v

    seen, dup, conf = {}, 0, []
    for r in rows(o.tx):
        k = tuple(r[c] for c in ("created_on", "settled_on", "amount", "currency", "status"))
        if r["txn_id"] in seen:
            dup += 1
            if seen[r["txn_id"]] != k:
                conf.append(r["txn_id"])
            continue
        seen[r["txn_id"]] = k
    rev, n, cur_tot = Decimal(0), 0, {}
    info = {}
    for tid, (cr, st, am, cu, status) in seen.items():
        info[tid] = (status, cu)
        if status.upper() != o.status.upper() or not st:
            continue
        d = day(st)
        if not inm(d):
            continue
        usd = amt(am) * rate(d, cu)
        rev += usd
        n += 1
        cur_tot[cu] = cur_tot.get(cu, Decimal(0)) + usd

    ref, nr, rdup, orphan, unsettled = Decimal(0), 0, 0, [], []
    rseen = set()
    for r in rows(o.refunds):
        rid = r.get("refund_id") or (r["txn_id"], r["refunded_on"], r["amount"])
        if rid in rseen:
            rdup += 1
            continue
        rseen.add(rid)
        d = day(r["refunded_on"])
        if not inm(d):
            continue
        if r["txn_id"] not in info:
            orphan.append(r["txn_id"])
            continue
        if info[r["txn_id"]][0].upper() != o.status.upper():
            unsettled.append(r["txn_id"])
        ref += amt(r["amount"]) * rate(d, info[r["txn_id"]][1])
        nr += 1

    q = lambda v: v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    net = float(q(rev - ref))
    print("unique_txn=%d dup_rows_dropped=%d conflicting_dups=%s | revenue_txns=%d revenue_usd=%s by_cur=%s | "
          "refunds_applied=%d refunds_usd=%s dup_refund_rows=%d orphan_refunds=%s refunds_on_non_%s_txn=%s | net_usd=%.2f"
          % (len(seen), dup, conf or "none", n, q(rev), {k: str(q(v)) for k, v in cur_tot.items()},
             nr, q(ref), rdup, orphan or "none", o.status, unsettled or "none", net), file=sys.stderr)
    ans = {"net_usd": net, "transactions": n, "refunds": nr}
    if not o.dry:
        os.makedirs(os.path.dirname(o.out) or ".", exist_ok=True)
        with open(o.out, "w") as f:
            json.dump(ans, f)
    print(json.dumps(ans))


if __name__ == "__main__":
    main()
