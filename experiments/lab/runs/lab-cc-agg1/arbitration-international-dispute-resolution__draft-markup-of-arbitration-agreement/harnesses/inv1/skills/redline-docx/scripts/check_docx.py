#!/usr/bin/env python3
"""Check a tracked-changes .docx: python3 -I check_docx.py <file.docx> [...] [--terms Term ...]

Reopens each file, reads it in the accepted and rejected revision views (pandoc),
and prints OK / INFO / WARN / FAIL lines. Exit 1 only on FAIL. Every WARN needs a
decision by the author; nothing here judges legal meaning.
"""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
LEFTOVER = re.compile(r"\{\.(insertion|deletion)|author=|\{\{|\}\}|\{%|%\}")
CROSS_REF = re.compile(r"Sections?\s+((?:\d+\.\d+(?:\([a-z]+\))?)(?:(?:,\s*|,?\s+(?:and|or)\s+)\d+\.\d+(?:\([a-z]+\))?)*)")
HEADING = re.compile(r"^\s*Section (\d+(?:\.\d+)+)\s*[—-]")
EXTERNAL = re.compile(r"^\s*(?:of|in|under) the [A-Z][\w-]*(?:\s+[A-Z][\w-]*)*\s+(?:Agreement|Contract|Instrument)\b")


def view(path, mode):
    r = subprocess.run(["pandoc", str(path), "-t", "plain", "--wrap=none",
                        f"--track-changes={mode}"], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"pandoc {mode} view failed: {r.stderr.strip()}")
    return r.stdout


def check(path, terms):
    p = Path(path)
    if not p.is_file() or p.stat().st_size == 0:
        print(f"FAIL {p}: missing or empty")
        return False
    try:
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None:
                print(f"FAIL {p}: corrupt zip member")
                return False
            root = ET.fromstring(z.read("word/document.xml"))
    except (zipfile.BadZipFile, ET.ParseError, KeyError) as e:
        print(f"FAIL {p}: not a readable .docx ({e})")
        return False

    ok = True
    ins = root.findall(f".//{W}ins")
    dels = root.findall(f".//{W}del")
    authors = {el.get(f"{W}author") for el in ins + dels}
    print(f"INFO {p.name}: {len(ins)} insertions, {len(dels)} deletions, authors={sorted(a or '<none>' for a in authors)}")
    if not ins and not dels:
        print(f"WARN {p.name}: no tracked changes found; a redline is expected to carry revisions")
    if any(el.get(f"{W}author") is None for el in ins + dels):
        print(f"WARN {p.name}: some revisions have no author attribute")

    try:
        accepted = view(p, "accept")
        rejected = view(p, "reject")
    except RuntimeError as e:
        print(f"FAIL {p.name}: {e}")
        return False

    for name, text in (("accepted", accepted), ("rejected", rejected)):
        for n, line in enumerate(text.splitlines(), 1):
            if LEFTOVER.search(line):
                print(f"FAIL {p.name} {name} view line {n}: leftover markup: {line[:120]}")
                ok = False

    defined = set()
    referenced = {}
    for n, line in enumerate(accepted.splitlines(), 1):
        m = HEADING.match(line)
        if m:
            defined.add(m.group(1))
        for ref in CROSS_REF.finditer(line):
            if EXTERNAL.match(line[ref.end():]):
                continue
            for num in re.findall(r"\d+\.\d+", ref.group(1)):
                referenced.setdefault(num, n)
        if "[" in line and not re.match(r"^\s*\[(Comment|HWC)", line):
            print(f"WARN {p.name} accepted view line {n}: bracketed text outside a comment: {line.strip()[:120]}")
    for num in sorted(set(referenced) - defined, key=lambda s: [int(x) for x in s.split(".")]):
        print(f"WARN {p.name} accepted view line {referenced[num]}: 'Section {num}' has no matching heading in accepted text")

    print(f"INFO {p.name}: accepted view {len(accepted.split())} words, rejected view {len(rejected.split())} words")
    for term in terms:
        in_acc = [n for n, l in enumerate(accepted.splitlines(), 1) if re.search(rf"\b{re.escape(term)}\b", l)]
        in_rej = len(re.findall(rf"\b{re.escape(term)}\b", rejected))
        defs = len(re.findall(rf"[“\"]{re.escape(term)}[”\"]", accepted))
        print(f"INFO {p.name} term '{term}': accepted={len(in_acc)} rejected={in_rej} defined_in_accepted={defs} lines={in_acc[:12]}")
        if in_acc and defs == 0:
            print(f"WARN {p.name}: '{term}' is used in the accepted view but never defined there")
    return ok


def main(argv):
    terms = []
    if "--terms" in argv:
        i = argv.index("--terms")
        terms = argv[i + 1:]
        argv = argv[:i]
    if not argv:
        print(__doc__)
        return 2
    results = [check(f, terms) for f in argv]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
