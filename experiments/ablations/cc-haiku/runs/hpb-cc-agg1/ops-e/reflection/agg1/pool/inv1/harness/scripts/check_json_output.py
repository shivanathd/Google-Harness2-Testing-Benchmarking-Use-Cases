"""Check a JSON deliverable: it parses, is an object, has exactly the named keys, and each value has the named type.

Usage: python3 -I scripts/check_json_output.py <path> <name:type> [<name:type> ...]
Types: int, float, str, bool, list, dict. Prints OK and exits 0 when clean;
otherwise prints every problem to stderr and exits 1.
"""
import json
import os
import sys

TYPES = {'int': int, 'float': (int, float), 'str': str, 'bool': bool, 'list': list, 'dict': dict}


def check(path, specs):
    if not os.path.isfile(path):
        return [f'missing file: {path}']
    try:
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return [f'not valid JSON: {exc}']
    if not isinstance(data, dict):
        return [f'top level is {type(data).__name__}, expected an object']

    expected = {}
    for spec in specs:
        name, _, typ = spec.partition(':')
        if typ not in TYPES:
            return [f'bad spec {spec!r}: type must be one of {", ".join(TYPES)}']
        expected[name] = typ

    problems = [f'unexpected key: {name}' for name in sorted(set(data) - set(expected))]
    for name, typ in expected.items():
        if name not in data:
            problems.append(f'missing key: {name}')
            continue
        value = data[name]
        ok = isinstance(value, TYPES[typ]) and not (typ in ('int', 'float') and isinstance(value, bool))
        if not ok:
            problems.append(f'{name} is {type(value).__name__} {value!r}, expected {typ}')
    return problems


def main(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    problems = check(argv[1], argv[2:])
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print(f'OK {argv[1]}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
