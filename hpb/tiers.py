"""Medium and hard HPB tasks. Each generator returns (workspace files, expected, prompt)."""

from __future__ import annotations

import csv
import datetime as dt
import gzip
import io
import json
import math
import random
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal

UTC = dt.timezone.utc
CENT = Decimal("0.01")


def _csv(header, rows) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue()


def _fmt_amount(rng, amt: Decimal) -> str:
    return rng.choice((f"{amt:.2f}", f"{amt:,.2f}"))


# ------------------------------------------------------------ data / medium

def data_medium(seed: int = 41):
    rng = random.Random(seed)
    days = [dt.date(2026, 8, 1) + dt.timedelta(d) for d in range(92)]  # Aug..Oct
    fx = {}
    rows_fx = []
    for day in days:
        for cur, base in (("USD", 1.0), ("EUR", 1.085), ("INR", 0.01195)):
            r = Decimal("1") if cur == "USD" else Decimal(str(round(base * (1 + rng.uniform(-.02, .02)), 6)))
            fx[(day, cur)] = r
            rows_fx.append([day.isoformat(), cur, f"{r}"])
    txns, net, counted, settled = [], Decimal(0), 0, []
    for i in range(40):
        cur = rng.choice(("USD", "USD", "EUR", "INR"))
        amt = Decimal(rng.randint(1000, 300000)) / 100 * (80 if cur == "INR" else 1)
        created = rng.choice(days[10:80])
        status = rng.choices(("SETTLED", "VOID", "PENDING"), (0.78, 0.1, 0.12))[0]
        settled_on = created + dt.timedelta(rng.randint(0, 6)) if status == "SETTLED" else None
        row = [f"S{i:03d}", created.isoformat(), settled_on.isoformat() if settled_on else "",
               _fmt_amount(rng, amt), cur, status]
        txns.append(row)
        if rng.random() < 0.15:
            txns.append(list(row))
        if settled_on:
            settled.append((row[0], amt, cur, settled_on))
            if settled_on.month == 9:
                net += amt * fx[(settled_on, cur)]
                counted += 1
    rng.shuffle(txns)
    refunds, n_ref = [], 0
    for j, (tid, amt, cur, settled_on) in enumerate(rng.sample(settled, 10)):
        when = min(settled_on + dt.timedelta(rng.randint(0, 30)), days[-1])  # never before settlement
        part = (amt * Decimal(rng.choice((25, 50, 100))) / 100).quantize(CENT)
        refunds.append([f"R{j:02d}", tid, when.isoformat(), f"{part:.2f}"])
        if when.month == 9:
            net -= part * fx[(when, cur)]
            n_ref += 1
    files = {
        "transactions.csv": _csv(["txn_id", "created_on", "settled_on", "amount", "currency", "status"], txns),
        "fx_daily.csv": _csv(["date", "currency", "usd_per_unit"], rows_fx),
        "refunds.csv": _csv(["refund_id", "txn_id", "refunded_on", "amount"], refunds),
    }
    exp = {"net_usd": float(net.quantize(CENT, ROUND_HALF_UP)), "transactions": counted,
           "refunds": n_ref}
    prompt = (
        "Compute September 2026 net revenue in USD from transactions.csv, refunds.csv and "
        "fx_daily.csv. Revenue is recognised on the settled_on date for SETTLED transactions, "
        "converted at that day's rate. Refunds (in the original transaction's currency) "
        "reduce revenue in the month they were issued, converted at the refund day's rate. "
        "A txn_id identifies one transaction. Write output/answer.json as "
        '{"net_usd": <number, 2 decimals>, "transactions": <recognised transactions>, '
        '"refunds": <refunds applied>}.'
    )
    return files, exp, prompt


# ------------------------------------------------------------ data / hard

POLICY = """# Revenue recognition policy (finance ops)

1. Revenue is recognised when a charge is `captured`. Use the `captured_at` timestamp
   converted to UTC to decide the month. `authorized` and `voided` charges are not revenue.
2. `amount_minor` is in the currency's minor unit: cents for USD and EUR, paise for INR.
   JPY has no minor unit, so its `amount_minor` is whole yen.
3. Convert to USD with fx.csv (one rate per currency for the month).
4. Charges from customers flagged `is_test = true` in customers.csv are excluded everywhere,
   including chargebacks.
5. A chargeback (chargebacks.csv) reverses the full original charge and costs a 15.00 USD
   fee. Both are booked in the month of `chargeback_at` (UTC), whenever the charge was made.
6. Round only the final figure to cents.
"""


def data_hard(seed: int = 53):
    rng = random.Random(seed)
    rates = {"USD": Decimal("1"), "EUR": Decimal("1.0850"), "INR": Decimal("0.01195"),
             "JPY": Decimal("0.00668")}
    customers = [(f"C{i:02d}", rng.random() < 0.2) for i in range(14)]
    test_ids = {c for c, t in customers if t}
    offsets = (dt.timedelta(0), dt.timedelta(hours=-5), dt.timedelta(hours=9),
               dt.timedelta(hours=5, minutes=30))
    rows, charges, net, counted = [], {}, Decimal(0), 0
    for i in range(45):
        cust = rng.choice(customers)[0]
        cur = rng.choice(("USD", "EUR", "INR", "JPY"))
        major = Decimal(rng.randint(1000, 200000)) / 100
        if cur == "INR":
            major *= 80
        if cur == "JPY":
            major = Decimal(int(major * 150))
            minor = int(major)
        else:
            minor = int(major * 100)
        status = rng.choices(("captured", "authorized", "voided"), (0.75, 0.15, 0.1))[0]
        # cluster some timestamps around month boundaries so the UTC conversion matters
        if rng.random() < 0.3:
            base = rng.choice((dt.datetime(2026, 9, 1, tzinfo=UTC), dt.datetime(2026, 10, 1, tzinfo=UTC)))
            t = base + dt.timedelta(hours=rng.uniform(-8, 8))
        else:
            t = dt.datetime(2026, rng.choice((8, 9, 9, 10)), rng.randint(2, 27), rng.randint(0, 23),
                            tzinfo=UTC)
        off = rng.choice(offsets)
        stamp = (t + off).replace(tzinfo=dt.timezone(off)).isoformat(timespec="minutes")
        cid = f"ch_{i:03d}"
        rows.append([cid, cust, cur, minor, status, stamp])
        usd = major * rates[cur]
        charges[cid] = (cust, usd, status, t)
        if status == "captured" and t.month == 9 and cust not in test_ids:
            net += usd
            counted += 1
    # Guarantee the is_test exclusion matters for revenue, not only for chargebacks:
    # two captured September charges from a test customer (never counted).
    if not test_ids:  # promote one customer and back out what was counted for it
        tcust = customers[0][0]
        for c, (cust, usd, st, t) in charges.items():
            if cust == tcust and st == "captured" and t.month == 9:
                net -= usd
                counted -= 1
        test_ids.add(tcust)
        customers = [(c, c == tcust or t) for c, t in customers]
    tcust = sorted(test_ids)[0]
    for i, amt in ((90, 1250), (91, 48000)):
        t = dt.datetime(2026, 9, 12 + i % 2, 15, tzinfo=UTC)
        rows.append([f"ch_{i:03d}", tcust, "USD", amt * 100, "captured", t.isoformat(timespec="minutes")])
    cbs, n_cb = [], 0
    captured = [c for c, v in charges.items() if v[2] == "captured"]
    for j, cid in enumerate(rng.sample(captured, 9)):
        t = charges[cid][3] + dt.timedelta(hours=rng.uniform(2, 24 * 30))  # never before capture
        cbs.append([f"cb_{j}", cid, t.isoformat(timespec="minutes").replace("+00:00", "Z")])
        cust, usd, _, _ = charges[cid]
        if t.month == 9 and cust not in test_ids:
            net -= usd + Decimal("15.00")
            n_cb += 1
    files = {
        "POLICY.md": POLICY,
        "charges.csv": _csv(["charge_id", "customer_id", "currency", "amount_minor", "status",
                             "captured_at"], rows),
        "customers.csv": _csv(["customer_id", "is_test"],
                              [[c, "true" if t else "false"] for c, t in customers]),
        "chargebacks.csv": _csv(["chargeback_id", "charge_id", "chargeback_at"], cbs),
        "fx.csv": _csv(["currency", "usd_per_unit"], [[c, f"{r}"] for c, r in rates.items()]),
    }
    exp = {"net_usd": float(net.quantize(CENT, ROUND_HALF_UP)), "transactions": counted,
           "chargebacks": n_cb}
    prompt = (
        "Finance needs the September 2026 net revenue figure. Follow POLICY.md in the "
        "workspace exactly. Write output/answer.json as {\"net_usd\": <number, 2 decimals>, "
        "\"transactions\": <charges recognised as September revenue, counted even if later "
        "charged back>, \"chargebacks\": "
        "<chargebacks booked in September>}."
    )
    return files, exp, prompt


# ------------------------------------------------------------ ops / medium

def ops_medium(seed: int = 61):
    rng = random.Random(seed)
    start = dt.datetime(2026, 10, 6, 8, tzinfo=UTC)
    end = start + dt.timedelta(hours=4)
    users = ("ana", "ben", "cai", "dev", "eli", "fay", "gus", "hal", "ivy")
    codes = ("E401", "E409", "E500", "E503")
    tzs = (dt.timedelta(0), dt.timedelta(hours=2), dt.timedelta(hours=-4))
    events = []  # (utc time, line[, continuation lines])
    final = {}
    for n in range(110):
        rid = f"r{seed}{n:04d}"
        user = rng.choice(users)
        t = start - dt.timedelta(hours=3) + dt.timedelta(seconds=rng.randrange(10 * 3600))
        attempts = rng.choice((1, 1, 2, 3))
        for a in range(1, attempts + 1):
            fails = rng.random() < (0.55 if a < attempts else 0.35)
            off = rng.choice(tzs)
            ts = (t + off).replace(tzinfo=dt.timezone(off)).isoformat(timespec="seconds")
            code = rng.choice(codes)
            if fails:
                line = f"{ts} ERROR req={rid} user={user} attempt={a} code={code} msg=failed"
                extra = ["  Traceback (most recent call last):",
                         f"  UpstreamError: ERROR code={rng.choice(codes)} user={rng.choice(users)}"] \
                    if rng.random() < 0.3 else []
            else:
                line = f"{ts} INFO req={rid} user={user} attempt={a} status=200 msg=ok"
                extra = []
            events.append((t, line, extra))
            final[rid] = (t, fails, user, code)
            t += dt.timedelta(seconds=rng.randint(2, 90))
        if rng.random() < 0.2:
            off = rng.choice(tzs)
            ts = (t + off).replace(tzinfo=dt.timezone(off)).isoformat(timespec="seconds")
            events.append((t, f"{ts} INFO user={user} msg=cache warm after ERROR code=E500", []))
    events.sort(key=lambda e: e[0])
    failed = [(u, c) for (t, f, u, c) in final.values() if f and start <= t < end]
    cnt = Counter(c for _, c in failed).most_common()
    if len(cnt) > 1 and cnt[0][1] == cnt[1][1]:
        t = start + dt.timedelta(minutes=3)
        events.append((t, f"{t.isoformat(timespec='seconds')} ERROR req=rx999 user=ana attempt=1 "
                          f"code={cnt[0][0]} msg=failed", []))
        failed.append(("ana", cnt[0][0]))
    # rotate: oldest third -> app.log.2.gz, middle -> app.log.1, newest -> app.log
    lines = [[line] + extra for _, line, extra in events]
    k = len(lines) // 3
    chunks = ["\n".join(x for grp in part for x in grp) + "\n"
              for part in (lines[:k], lines[k:2 * k], lines[2 * k:])]
    files = {"logs/app.log.2.gz": gzip.compress(chunks[0].encode(), mtime=0),
             "logs/app.log.1": chunks[1], "logs/app.log": chunks[2]}
    exp = {"failed": len(failed), "users": len({u for u, _ in failed}),
           "top_code": Counter(c for _, c in failed).most_common(1)[0][0]}
    prompt = (
        "logs/ holds the rotated logs of one service (app.log is newest; app.log.N are older; "
        "some are gzip-compressed). Timestamps carry UTC offsets. Each request (req=) may be "
        "retried; a request FAILED if its last logged attempt is an ERROR line. Consider "
        f"requests whose last attempt falls in {start:%Y-%m-%d %H:%M} (inclusive) to "
        f"{end:%H:%M} (exclusive) UTC. Find the number of failed requests, the number of "
        "distinct users with a failed request, and the most frequent error code among the "
        'failed requests\' last attempts. Write output/answer.json as {"failed": <int>, '
        '"users": <int>, "top_code": "<code>"}.'
    )
    return files, exp, prompt


# ------------------------------------------------------------ ops / hard

RUNBOOK = """# Gateway fleet runbook (excerpt)

- Access logs are JSON lines in logs/<service>.jsonl (billing's is gzip-compressed).
- The log shipper occasionally truncates a line; skip lines that are not valid JSON.
- `/healthz` is the load balancer's probe. Exclude it from every traffic statistic.
- Errors are responses with status >= 500. 4xx responses are client errors, not errors.
- Schema change: since 2026-10-04 09:00 UTC billing logs `latency_s` (seconds, float)
  instead of `latency_ms`. Other services always log `latency_ms`.
"""


def ops_hard(seed: int = 71):
    rng = random.Random(seed)
    start = dt.datetime(2026, 10, 4, 6, tzinfo=UTC)
    end = start + dt.timedelta(hours=6)
    switch = dt.datetime(2026, 10, 4, 9, tzinfo=UTC)
    routes = {"gateway": ("/v1/orders", "/v1/cart", "/healthz"),
              "search": ("/v1/search", "/v1/suggest", "/healthz"),
              "billing": ("/v1/invoice", "/v1/charge", "/healthz")}
    exp, files = {}, {}
    for svc, rts in routes.items():
        lines, lat, errs = [], [], 0
        for _ in range(260):
            t = start - dt.timedelta(hours=2) + dt.timedelta(seconds=rng.randrange(10 * 3600))
            route = rng.choices(rts, (0.4, 0.35, 0.25))[0]
            status = rng.choices((200, 201, 404, 429, 500, 503), (60, 10, 8, 5, 9, 8))[0]
            ms = int(rng.lognormvariate(5.0 if svc != "search" else 4.3, 0.6))
            off = rng.choice((dt.timedelta(0), dt.timedelta(hours=1), dt.timedelta(hours=-3)))
            rec = {"ts": (t + off).replace(tzinfo=dt.timezone(off)).isoformat(timespec="seconds"),
                   "route": route, "status": status}
            if svc == "billing" and t >= switch:
                rec["latency_s"] = round(ms / 1000, 3)
            else:
                rec["latency_ms"] = ms
            text = json.dumps(rec)
            if rng.random() < 0.04:  # truncated by the shipper: excluded everywhere
                lines.append((t, text[: rng.randint(10, len(text) - 5)]))
                continue
            lines.append((t, text))
            if start <= t < end and route != "/healthz":
                lat.append(round(rec["latency_s"] * 1000) if "latency_s" in rec else ms)
                errs += status >= 500
        lines.sort()
        body = "\n".join(x for _, x in lines) + "\n"
        n = len(lat)
        p95 = sorted(lat)[math.ceil(0.95 * n) - 1]
        exp[svc] = {"requests": n, "error_rate": round(errs / n, 4), "p95_ms": p95}
        if svc == "billing":
            files["logs/billing.jsonl.gz"] = gzip.compress(body.encode(), mtime=0)
        else:
            files[f"logs/{svc}.jsonl"] = body
    files["RUNBOOK.md"] = RUNBOOK
    prompt = (
        "Produce the traffic report for 2026-10-04 06:00 (inclusive) to 12:00 (exclusive) UTC "
        "for the services in logs/, following RUNBOOK.md. For each service give requests "
        "(count), error_rate (errors / requests, rounded to 4 decimals) and p95_ms (95th "
        "percentile latency in milliseconds by the nearest-rank method, as an integer). Write "
        'output/answer.json as {"gateway": {"requests": .., "error_rate": .., "p95_ms": ..}, '
        '"search": {...}, "billing": {...}}.'
    )
    return files, exp, prompt


# ------------------------------------------------------------ swe / medium (invoicing)

SWE_M_FILES = {
    "invoicing/__init__.py": "",
    "invoicing/models.py": '''from dataclasses import dataclass


@dataclass
class LineItem:
    description: str
    qty: int
    unit_price: str  # decimal string, e.g. "19.99"
    discount_pct: int = 0
''',
    "invoicing/tax.py": '''RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}


def rate_for(region):
    return RATES[region]
''',
    "invoicing/totals.py": '''from .tax import rate_for


def line_total(item):
    return round(item.qty * float(item.unit_price), 2)


def compute_totals(items, region):
    subtotal = sum(line_total(i) for i in items)
    tax = round(subtotal * float(rate_for(region)), 2)
    discount = round(sum(line_total(i) * i.discount_pct / 100 for i in items), 2)
    total = subtotal + tax - discount
    return {"subtotal": subtotal, "discount": discount, "tax": tax, "total": total}
''',
    "docs/ROUNDING.md": """# Money rules

- All money is computed with `decimal.Decimal`, never float, and every amount that
  `compute_totals` returns is a string with exactly two decimals, e.g. "12.30".
- Line gross = qty x unit_price, rounded half-up to cents.
- Line discount = line gross x discount_pct / 100, rounded half-up to cents.
- subtotal = sum of line gross; discount = sum of line discounts.
- tax = (subtotal - discount) x the region's rate, rounded half-up to cents.
- total = subtotal - discount + tax.
- Region codes are case-insensitive. An unknown region raises ValueError.
""",
    "ISSUE.md": """# #142 Invoice totals wrong for discounted EU invoices

Reported by finance:

- `compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")` raises KeyError.
- With "EU" the tax is charged on the undiscounted amount.
- Totals are sometimes a cent off (float rounding), e.g. a 0.125 unit price.

Please make `invoicing.totals.compute_totals` follow docs/ROUNDING.md.
""",
    "tests/test_totals.py": '''from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"
''',
}

SWE_M_PRELUDE = '''
from decimal import Decimal, ROUND_HALF_UP
from invoicing.models import LineItem
from invoicing.totals import compute_totals
from invoicing import tax as taxmod
_R = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}
def _q(x): return x.quantize(Decimal("0.01"), ROUND_HALF_UP)
def ref(items, region):
    rate = Decimal(_R[region.upper()])
    sub = disc = Decimal(0)
    for i in items:
        g = _q(Decimal(i.qty) * Decimal(i.unit_price)); sub += g
        disc += _q(g * Decimal(i.discount_pct) / 100)
    t = _q((sub - disc) * rate)
    return {k: f"{v:.2f}" for k, v in (("subtotal", sub), ("discount", disc), ("tax", t), ("total", sub - disc + t))}
def same(items, region): return compute_totals(items, region) == ref(items, region)
L = LineItem
'''

SWE_M_CASES = [
    ("basic_us", 'same([L("a", 2, "10.00")], "US")'),
    ("eu_discount", 'same([L("w", 3, "19.99", 10)], "EU")'),
    ("lowercase_region", 'same([L("w", 3, "19.99", 10)], "eu")'),
    ("half_up_line", 'compute_totals([L("x", 1, "0.125")], "US")["subtotal"] == "0.13"'),
    ("float_cents", 'compute_totals([L("a", 3, "0.10"), L("b", 1, "0.20")], "US")["total"] == "0.50"'),
    ("multi_line_in", 'same([L("a", 7, "3.33", 5), L("b", 1, "99.99", 15), L("c", 4, "0.07")], "IN")'),
    ("tax_after_discount", 'compute_totals([L("p", 1, "100.00", 50)], "UK")["tax"] == "10.00"'),
    ("unknown_region", 'raises(lambda: compute_totals([L("a", 1, "1.00")], "XX"))'),
    ("strings", 'all(isinstance(v, str) for v in compute_totals([L("a", 1, "1.00")], "US").values())'),
    ("empty", 'compute_totals([], "UK") == {"subtotal": "0.00", "discount": "0.00", "tax": "0.00", "total": "0.00"}'),
]

# ------------------------------------------------------------ swe / hard (stock CLI)

SWE_H_FILES = {
    "stock/__init__.py": "",
    "stock/store.py": '''import json


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
''',
    "stock/ops.py": '''def add(data, sku, qty):
    data[sku] = data.get(sku, 0) + qty
    return data


def remove(data, sku, qty):
    data[sku] = data.get(sku, 0) - qty
    return data
''',
    "stock/cli.py": '''import argparse

from . import ops, store


def main(argv=None):
    p = argparse.ArgumentParser(prog="stock")
    p.add_argument("--file", default="stock.json")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("sku")
    a.add_argument("qty", type=int)
    r = sub.add_parser("remove")
    r.add_argument("sku")
    r.add_argument("qty", type=int)
    sub.add_parser("report")
    args = p.parse_args(argv)
    data = store.load(args.file)
    if args.cmd == "add":
        ops.add(data, args.sku, args.qty)
    elif args.cmd == "remove":
        ops.remove(data, args.sku, args.qty)
    else:
        for sku in sorted(data):
            print(f"{sku}\\t{data[sku]}")
        return 0
    store.save(args.file, data)
    return 0
''',
    "ISSUE.md": """# Inventory CLI: three fixes for the next release

1. `stock report` crashes when the stock file does not exist yet or is empty. Treat both
   as an empty inventory (`store.load` returns `{}`).
2. `remove` lets quantities go below zero and silently creates unknown SKUs. `ops.remove`
   must raise ValueError instead and leave the data unchanged. `ops.add` must likewise
   raise ValueError for a quantity that is not positive. In the CLI, any such error prints
   `error: <message>` to stderr, returns exit status 1 and leaves the file unchanged.
3. Feature: `stock report --low N` lists only SKUs with quantity < N, sorted by quantity
   ascending, then by SKU. The plain `stock report` output (`SKU<TAB>QTY` lines sorted by
   SKU) must not change -- other tools parse it.

`stock.cli.main(argv)` returns the exit status.
""",
    "tests/test_cli.py": '''import json

from stock.cli import main


def test_add_then_file(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{}")
    assert main(["--file", str(f), "add", "bolt", "3"]) == 0
    assert json.loads(f.read_text()) == {"bolt": 3}
''',
}

SWE_H_PRELUDE = '''
import contextlib, io, json, os, tempfile
from stock import cli, ops, store
def tmpfile(content=None):
    d = tempfile.mkdtemp(); p = os.path.join(d, "stock.json")
    if content is not None:
        open(p, "w").write(content)
    return p
def run_cli(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = cli.main(argv)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
    return (code or 0), out.getvalue(), err.getvalue()
def remove_keeps_data():
    d = {"a": 1}
    try:
        ops.remove(d, "a", 5)
    except ValueError:
        pass
    return d == {"a": 1}
def cli_remove_error():
    p = tmpfile('{"a": 1}')
    code, out, err = run_cli(["--file", p, "remove", "a", "5"])
    return code == 1 and err.startswith("error:") and json.load(open(p)) == {"a": 1}
def cli_add_bad():
    p = tmpfile('{"a": 1}')
    code, out, err = run_cli(["--file", p, "add", "a", "0"])
    return code == 1 and err.startswith("error:") and json.load(open(p)) == {"a": 1}
def cli_add_report():
    p = tmpfile()
    run_cli(["--file", p, "add", "nut", "4"]); run_cli(["--file", p, "add", "bolt", "2"])
    return run_cli(["--file", p, "report"]) == (0, "bolt\\t2\\nnut\\t4\\n", "")
'''

SWE_H_CASES = [
    ("load_missing", "store.load(tmpfile()) == {}"),
    ("load_empty", 'store.load(tmpfile("")) == {}'),
    ("add_accumulates", 'ops.add({"A": 1}, "A", 2) == {"A": 3}'),
    ("add_nonpositive", 'raises(lambda: ops.add({}, "A", 0))'),
    ("remove_ok", 'ops.remove({"A": 5}, "A", 2) == {"A": 3}'),
    ("remove_too_many", 'raises(lambda: ops.remove({"A": 1}, "A", 2))'),
    ("remove_unknown", 'raises(lambda: ops.remove({}, "Z", 1))'),
    ("remove_keeps_data", "remove_keeps_data()"),
    ("report_format", 'run_cli(["--file", tmpfile(\'{"b": 2, "a": 10}\'), "report"]) == (0, "a\\t10\\nb\\t2\\n", "")'),
    ("report_missing_file", 'run_cli(["--file", tmpfile(), "report"])[:2] == (0, "")'),
    ("cli_remove_error", "cli_remove_error()"),
    ("cli_add_bad", "cli_add_bad()"),
    ("report_low", 'run_cli(["--file", tmpfile(\'{"c": 1, "a": 3, "b": 1, "d": 9}\'), "report", "--low", "4"])[1] == "b\\t1\\nc\\t1\\na\\t3\\n"'),
    ("add_then_report", "cli_add_report()"),
]
