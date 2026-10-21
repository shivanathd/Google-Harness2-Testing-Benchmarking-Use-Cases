#!/usr/bin/env python3
"""Count log events of one level inside a UTC window.

usage: log_window_stats.py LOG --start YYYY-MM-DDTHH:MM --end YYYY-MM-DDTHH:MM [--level ERROR] [--field user] [--field2 code]

Start/end are UTC (start inclusive, end exclusive). An event is a line that BEGINS with an
ISO-8601 timestamp + offset, then LEVEL, then [service], then key=value pairs. Indented
continuation lines (tracebacks) and the word ERROR inside msg= are NOT events.
Output: JSON with count, distinct field values, per-code counts, per-service counts, and
every counted event. Lines that are neither events nor indented continuations, and events
with no offset, are listed under "problems" (exit code 1 if any) -- inspect them.
"""
import argparse, collections, datetime as dt, json, re, sys

HEAD = re.compile(r'^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?)(Z|[+-]\d\d:?\d\d)?\s+([A-Z]+)\s+\[([^\]]*)\]\s*(.*)$')

def utc(s):
    s = s.strip()
    if len(s) == 16: s += ':00'
    t = dt.datetime.fromisoformat(s)
    return t.replace(tzinfo=dt.timezone.utc) if t.tzinfo is None else t.astimezone(dt.timezone.utc)

def main():
    a = argparse.ArgumentParser()
    a.add_argument('log'); a.add_argument('--start', required=True); a.add_argument('--end', required=True)
    a.add_argument('--level', default='ERROR'); a.add_argument('--field', default='user'); a.add_argument('--field2', default='code')
    a = a.parse_args()
    lo, hi = utc(a.start), utc(a.end)
    events, problems, levels = [], [], collections.Counter()
    for n, line in enumerate(open(a.log, encoding='utf-8', errors='replace'), 1):
        line = line.rstrip('\n')
        if not line.strip() or line[0] in ' \t': continue
        m = HEAD.match(line)
        if not m: problems.append([n, 'unparsed', line]); continue
        ts, off, level, svc, rest = m.groups()
        if off is None: problems.append([n, 'no offset', line]); continue
        t = utc(ts + (off if off != 'Z' else '+00:00'))
        levels[level] += 1
        if level != a.level or not (lo <= t < hi): continue
        kv = dict(re.findall(r'(\w+)=(\S+)', rest.split(' msg=')[0]))
        events.append({'line': n, 'utc': t.strftime('%Y-%m-%dT%H:%M:%SZ'), 'service': svc, a.field: kv.get(a.field), a.field2: kv.get(a.field2)})
    f1 = {e[a.field] for e in events if e[a.field]}
    c2 = collections.Counter(e[a.field2] for e in events if e[a.field2])
    top = c2.most_common()
    json.dump({'count': len(events), 'distinct_' + a.field: len(f1), a.field + 's': sorted(f1),
               'by_' + a.field2: dict(top), 'top_tie': bool(len(top) > 1 and top[0][1] == top[1][1]),
               'by_service': dict(collections.Counter(e['service'] for e in events)),
               'levels_in_file': dict(levels), 'events': events, 'problems': problems}, sys.stdout, indent=1)
    print()
    sys.exit(1 if problems else 0)

main()
